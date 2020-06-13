from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, Http404
from django.conf import settings
from django.core.paginator import Paginator

#Sending order confirmation email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import Context,Template

# Use for customer section
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import *
from .forms import CustomerRegisterForm, UpdateProfileForm

from .models import *
from .forms import ShippingAddressForm
from django.core import serializers
import json


"""
------------------------------------------------------------
                   HOME PAGE
------------------------------------------------------------
""" 
def Store(request):
    products = Product.objects.all().order_by('-created_date')
    p_products = Paginator(products,12)
    page_number = request.GET.get('page')
    products_obj = p_products.get_page(page_number)
    try:
        slider = [
            get_object_or_404(Ads,remark='home-slider-1'),
            get_object_or_404(Ads,remark='home-slider-2'),
            get_object_or_404(Ads,remark='home-slider-3'),
        ]
        ads = {
            'home_top_right':get_object_or_404(Ads,remark='home-top-right'),
            'home_top_left':get_object_or_404(Ads,remark='home-top-left'),
            'home_bottom':get_object_or_404(Ads,remark='home-bottom')
        }
    except:
        slider = []
        ads = []
    context={
        'products':products_obj,
        'slider':slider,
        'ads':ads
    }
    return render(request, 'index.html',context)
"""
------------------------------------------------------------
                   PRODUCT DISPLAY SECTION
------------------------------------------------------------
""" 

def ProductDetail(request,slug):
    product = Product.objects.get(slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(slug=slug)
    p_products = Paginator(related_products,4)
    page_number = request.GET.get('page')
    products_obj = p_products.get_page(page_number)
    context={
        'product':product,
        'related_products':products_obj
    }
    return render(request, 'product.html',context)

def ProductByCategory(request,pk):
    category = Category.objects.get(id=pk)
    products = category.product_set.all().order_by('-created_date')
    context={
        'category':category,
        'products':products
    }
    return render(request, 'categories.html',context)

def SortProduct(request):
    if request.is_ajax() and request.POST['sort']:
        sort_type = request.POST['sort']
        category = Category.objects.get(id=request.POST['category'])
        if request.POST['sort'] == 'default':
            product = category.product_set.all().order_by('-created_date')
        else:
            product = category.product_set.all().order_by(sort_type)
        data = serializers.serialize('json', list(product))
        return HttpResponse(data,content_type='application/json')
    else:
        raise Http404
    
def SearchProduct(request):
    result = Product.objects.filter(name__icontains=request.GET['key'])
    context = {
        'products':result
    }
    return render(request, 'search-list.html',context)


"""
------------------------------------------------------------
                   CART AND CHECK OUT SECTION
------------------------------------------------------------
"""  
def Cart(request):
    items = []
    total_item = 0
    total_value = 0
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    #Example cart : {'3': {'quantity': 2}, '4': {'quantity': 6}, '5': {'quantity': 5}, '6': {'quantity': 1}}
    for key,value in cart.items():
        try:
            product = Product.objects.get(id=key, out_stock=False)
            items.append({
                'product':product,
                'quantity':value['quantity'],
                'get_total':product.price*value['quantity']
                })
            total_item += value['quantity']
            total_value += product.price * value['quantity']
        except:
            items = []
    order = {'get_cart_total':total_value,'get_cart_item':total_item}

    context={
        'items':items,
        'order':order,
    }
    return render(request, 'cart.html',context)

@allowed_users(allowed_roles=['customer','admin'])
def CheckOut(request):
    items = []
    total_item = 0
    total_value = 0
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    # Retrieve data from cookie
    # Example cart : {'3': {'quantity': 2}, '4': {'quantity': 6}, '5': {'quantity': 5}, '6': {'quantity': 1}}
    for key,value in cart.items():
        product = Product.objects.get(id=key, out_stock=False)
        items.append({
            'product':product,
            'quantity':value['quantity'],
            'get_total':product.price*value['quantity']
            })
        total_item += value['quantity']
        total_value += product.price * value['quantity']
    order = {'get_cart_total':total_value,'get_cart_item':total_item}
    

    # Create order , order items , sending confirmation email
    shipping_form = ShippingAddressForm(initial={
        'first_name':request.user.customer.first_name,
        'last_name':request.user.customer.last_name,
        'email':request.user.customer.email
        })
    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.POST)
        print(request.POST)
        print(request.user)
        if shipping_form.is_valid():
            
            create_order = Order.objects.create(customer=Customer.objects.get(user=request.user),
            transaction_id=CreateTransactionID(),
            payment_type=request.POST.get('payment_type'))
            create_order.save()
            for key,value in cart.items():
                product = Product.objects.get(id=key, out_stock=False)
                create_order_items = OrderItem.objects.create(product=product, order=create_order, quantity=value['quantity'])
                create_order_items.save()
            
            current_data = shipping_form.save(commit=False)
            current_data.order = create_order
            current_data.customer = create_order.customer
            current_data.save()
            shipping_form.save_m2m()

            # sending order confirmation email 
            OrderConfirmationEmail(request,create_order)
            
            return redirect(reverse('check-out-done'))
    context={
        'items':items,
        'order':order,
        'form' : shipping_form
    }
    return render(request, 'check-out.html',context)

@allowed_users(allowed_roles=['customer','admin'])
def CheckOutDone(request):
    return render(request,'check-out-done.html',{})

"""
------------------------------------------------------------
                   CUSTOMER SECTION
------------------------------------------------------------
"""  
@unauthenticated_user
def Register(request):
    form = CustomerRegisterForm()
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_name =  form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user, username=user_name, email=email)
            messages.success(request, 'Tai khoan ' + user_name + ' da duoc tao thanh cong')
            return redirect(reverse('login'))
    context = {'form':form}
    return render(request, 'customer/register.html', context)

@unauthenticated_user	
def LoginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect(reverse('store'))
		else:
			messages.info(request, 'Tai khoan hoac mat khau khong chinh xac')
	context = {}
	return render(request, 'customer/login.html', context)


def LogoutUser(request):
    logout(request)
    return redirect(reverse('store'))


@allowed_users(allowed_roles=['customer','admin'])
def CustomerPage(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer).order_by('-date_ordered')
    context = {
        'customer':customer,
        'orders':orders
        }
    return render(request, 'customer/customer-page.html', context)

@allowed_users(allowed_roles=['customer','admin'])
def UpdateCustomerProfile(request):
    customer = request.user.customer
    form = UpdateProfileForm(instance=customer)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            # customer.user.email = form.cleaned_data.get('email')
            # customer.user.save()
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(reverse('customer-page'))
    context = {
        'customer':customer,
        'form':form
    }
    return render(request, 'customer/update-profile-page.html',context)

@allowed_users(allowed_roles=['customer','admin'])
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse('customer-page'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = {
    'form':form
    }
    return render(request, 'customer/change-password.html',context)


"""
------------------------------------------------------------
                   EMAIL SECTION
------------------------------------------------------------
"""  

def OrderConfirmationEmail(request,order):
    if request.method =='POST':
        data = request.POST.copy()
        subject = "Personal Store - Order confirmation >>> " + str(order.transaction_id)
        from_email = settings.DEFAULT_FROM_EMAIL
        to = data.get('email')
        email_context = { 
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'address' : data.get('address'),
            'phone' : data.get('phone'),
            'created_data':data.get('date_added'),
            'transaction_id':order.transaction_id,
            'payment_type':order.payment_type,
            'cart_items':OrderItem.objects.filter(order=order),
            'total':order.get_cart_total
            }
        content = render_to_string('order-confirmation.html',email_context)        
        msg = EmailMultiAlternatives(subject, content, from_email, [to])
        msg.content_subtype = "html"
        msg.send()


"""
------------------------------------------------------------
                   EXTRA
------------------------------------------------------------
"""  
# Create transaction ID when create Order
def CreateTransactionID():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%d") + now.strftime("%m") + now.strftime("%y") + now.strftime("%H") + now.strftime("%M") + now.strftime("%S") + now.strftime("%f")
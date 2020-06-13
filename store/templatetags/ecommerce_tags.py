from django import template
from store.models import Order, Customer, Category, OrderItem, ShippingAddress
import json
register = template.Library()
@register.filter
def vnd(value):
    try:
        s = list(str(round(value)))
        result = ''
        count = 0 
        while len(s) != 0 :
            result += s.pop()
            count += 1
            if count % 3 == 0:
                result += ","
        if result[-1] == ',':
            result = result[:-1]
        return "VND " + result[::-1]
    except:
        return value
# add class to django template exp: {{ field|addclass:"class-name"}}
@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})
@register.filter
def replace_by_spc(value, arg):
    return value.replace(arg,' ')



@register.inclusion_tag('customer/order_items.html')
def show_order_items (order):
    items = order.orderitem_set.all()
    return {'items':items}

@register.inclusion_tag('customer/shipping_address.html')
def show_shipping_address (order):
    shipping_address = ShippingAddress.objects.get(order=order)
    return {'address':shipping_address}


@register.simple_tag(takes_context=True)
def cart_items(context):
    request = context['request']
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = 0
    for i in cart:
        items += cart[i]['quantity']
    return items

@register.simple_tag
def category_menu():
    try:
        return Category.objects.all()
    except:
        return []


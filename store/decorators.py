from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render 
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('store'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse('login'))
            groups = None 
            if request.user.groups.exists():
                groups = request.user.groups.all()
                for group in groups:
                    if group.name in allowed_roles:
                        return view_func(request, *args, **kwargs)    
            return render(request,'customer/not-authorize.html')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None 
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name 
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('There is an error occur')
    return wrapper_func

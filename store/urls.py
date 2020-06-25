from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',Store,name='store'),
    # ---- Product display Section -----
    path('product/<str:slug>',ProductDetail,name='product'),
    path('category/<str:pk>',ProductByCategory, name='category'),
    path('search-item/',SearchProduct,name='search'),
    path('sort-product/',SortProduct,name='sort-product'),

    # ---- Cart Section -----
    path('cart/',Cart,name='cart'),
    path('check-out/',CheckOut,name='check-out'),
    path('check-out-done/',CheckOutDone,name='check-out-done'),

    # ---- Customer Section -----
    path('register/',Register, name='register'),
    path('login/',LoginPage, name='login'),
    path('logout/',LogoutUser, name='logout'),
    path('customer/',CustomerPage, name='customer-page'),
    path('update_profile/',UpdateCustomerProfile, name='update-profile'),
    path('change_password/',ChangePassword, name='change-password'),
    path('password_reset/', auth_views.PasswordResetView.as_view( template_name='customer/password_reset.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view( template_name='customer/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='customer/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view( template_name='customer/password_reset_complete.html'), name='password_reset_complete')
    
]

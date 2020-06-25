from django.urls import path
from .views import *

urlpatterns = [
    path('',api_root),
    path('categories/',CategoryList.as_view(),name='category-list'),
    path('category/<int:pk>',CategoryDetail.as_view(),name='category-detail'),
    path('products/',ProductList.as_view(),name='product-list'),
    path('product/<int:pk>',ProductDetail.as_view(),name='product-detail'),
    path('orders/',OrderList.as_view(),name='order-list'),
    path('order/<int:pk>',OrderDetail.as_view(),name='order-detail'),
    path('customers/',CustomerList.as_view(), name='customer-list'),
    path('customer/<int:pk>',CustomerDetail.as_view(), name='customer-detail'),
    path('Ads/',AdsList.as_view(),name='ads-list'),
    path('Ads/<int:pk>',AdsDetail.as_view(),name='ads-detail'),
]
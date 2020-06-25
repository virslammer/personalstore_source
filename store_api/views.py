from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import generics, permissions
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import CustomerSerializer,ProductSerializer, CategorySerializer, AdsSerializer, OrderSerializer
from store.models import Customer,Product, Category, Ads, Order, OrderItem
# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'customers':reverse('customer-list',request=request, format=format),
        'products':reverse('product-list',request=request, format=format),
        'categories':reverse('category-list',request=request, format=format),
        'ads':reverse('ads-list',request=request, format=format),
        'orders':reverse('order-list',request=request, format=format)
    })
'''
---------------------------------------
    PRODUCT AND CATEGORY SECTION
---------------------------------------

'''
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


'''
---------------------------------------
    ORDER AND CUSTOMER SECTION
---------------------------------------

'''
class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetail(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

'''
---------------------------------------
    ADS SECTION
---------------------------------------

'''

class AdsList(generics.ListCreateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class AdsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
from rest_framework import serializers
from store.models import Customer,Product, Category, Ads, Order, OrderItem,ShippingAddress



'''
-------PRODUCT SECTION---------
'''
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    product_detail = serializers.HyperlinkedIdentityField(view_name='product-detail')
    class Meta:
        model=Product 
        fields = ['category','category_name','product_detail', 'name', 'summary','price','out_stock','image','status','created_date','slug']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = ['name','description','image','products']

'''
-------ORDER SECTION---------
'''

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['first_name','last_name','email','address','phone']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price =serializers.ReadOnlyField(source='product.price')
    order_transaction_id =serializers.ReadOnlyField(source='order.transaction_id')
    class Meta:
        model = OrderItem
        fields = ['product_name','product_price','product','quantity','date_added','order','order_transaction_id']
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer = serializers.SlugRelatedField(slug_field='username',read_only=True,many=False)
    shipping_address = ShippingAddressSerializer(many=False,read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model= Order 
        fields = ['customer','id','transaction_id','date_ordered','complete','payment_type','items','shipping_address']

'''
-------CUSTOMER SECTION---------
'''
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    order_list = OrderSerializer(many=True)
    class Meta:
        model = Customer 
        fields = ['url','id','username','first_name','last_name', 'email','order_list'  ]


'''
-------ADS SECTION---------
'''
class AdsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ads 
        fields = ['url','id','title','content','image','link_to','remark']
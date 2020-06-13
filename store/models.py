from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    email = models.EmailField(null=True, unique=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='customer-profile-pic', default='customer-profile-pic/default_profile.png')
    def __str__(self):
        return self.user.username
    @property
    def ProfilePicURL(self):
        try:
            url = self.profile_pic.url 
        except:
            url = ''
        return url

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True , upload_to='category')
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        return url

class Product(models.Model):
    STATUS = (
        ('Normal','Normal'),
        ('New','New'),
        ('Hot','Hot'),
        ('Sale','Sale'),
    )
    category = models.ForeignKey(Category,null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, unique=True)
    summary = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10 , decimal_places=0)
    out_stock = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True , upload_to='product')
    status = models.CharField(max_length=50,null=True, blank=True, choices=STATUS, default='Normal')
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='',editable=False)
    def save(self, *args, **kwargs): 
        self.slug = slugify(unidecode(self.name)) # Xoa dau tieng viet
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    payment_type = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.product)
    @property
    def get_product_quantity(self):
        return {'product':self.product,'quantity':self.quantity}

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Shipping Address"
    def __str__(self):
        return self.address

class Ads(models.Model):
    title = models.CharField(max_length=200,blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='ads')
    link_to = models.URLField(default='')
    remark = models.CharField(max_length=200,blank=True, null=True,unique=True, default=None)
    class Meta:
        verbose_name_plural = "Ads"
    def __str__(self):
        return self.remark
    @property
    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        return url

class Subcribe(models.Model):
    email = models.EmailField(unique=True)
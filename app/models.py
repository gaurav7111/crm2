from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models.signals import post_save


# Create your models here.
class ModelTest(TestCase):
    def setUpClass(cls):
        super(ModelTest, cls).setUpClass

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.IntegerField(null=True,blank=True)
    email = models.EmailField()
    profile_pic = models.ImageField(default="profile.png",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name 


class Tags(models.Model):
    name = models.CharField(max_length=200,null=True)   

    def __str__(self):
        return self.name 



class Product(models.Model):
    CATEGORY=(
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),

    )
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200,null=True,choices=CATEGORY)
    description = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)  
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name 



class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out For Delivery','Out For Delivery'),
        ('Deliverd','Deliverd'),

    )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)     
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)

    def __str__(self):
        return self.product.name 

    

    
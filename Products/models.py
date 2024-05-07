from django.db import models
from  Users.models import  User
STATECHOICE=(
    ('draft','Draft'),
    ('paid','Paid'),
    ('unsuccessful','Unsuccessful')
)

class Units(models.Model):
    Title = models.CharField(max_length=150)

class Categories(models.Model):
    Title = models.CharField(max_length=250)



class Products(models.Model):

    ProductId = models.CharField(max_length=150 , null=False,db_index=True )
    Price = models.FloatField(default=0,null=False)
    UnitsId = models.ForeignKey(Units , on_delete=models.CASCADE ,null=True)
    DicountPer = models.FloatField(default=1)
    Existance = models.BooleanField()
    CategoryId = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)


class Order(models.Model):

    OrderId =models.CharField(max_length=150)
    ProductId = models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    ProductNumber = models.IntegerField(default=1)
    total = models.FloatField()

class Cart(models.Model):

    CartId = models.CharField(max_length=150)
    Address = models.CharField(max_length=500)
    State = models.CharField(max_length=150,choices=STATECHOICE,default='draft')
    CustomerName = models.CharField(max_length=150)
    phoneNumber = models.CharField(max_length=25)
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)




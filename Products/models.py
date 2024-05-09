from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop import to_roman_numeral
from Users.models import User
from address.models import Address


STATECHOICE = (
    ('draft', 'Draft'),
    ('paid', 'Paid'),
    ('unsuccessful', 'Unsuccessful')
)

class Units(models.Model):
    Title = models.CharField(max_length=150)

class Categories(models.Model):
    CategoryId = models.CharField(max_length=50, default='')
    Title = models.CharField(max_length=250)
    ParentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)

@receiver(post_save, sender=Categories)
def set_addressId(sender, instance, created, **kwargs):
    if created:
        instance.CategoryId = to_roman_numeral(instance.id)
        instance.save()


class Products(models.Model):
    ProductId = models.CharField(max_length=150, null=False, db_index=True )
    Price = models.FloatField(default=0, null=False)
    UnitsId = models.ForeignKey(Units, on_delete=models.CASCADE, null=True)
    DicountPer = models.FloatField(default=1)
    Existance = models.BooleanField()
    CategoryId = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)


class Order(models.Model):
    OrderId =models.CharField(max_length=150)
    ProductId = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    ProductNumber = models.IntegerField(default=1)
    total = models.FloatField()

class Cart(models.Model):
    CartId = models.CharField(max_length=150)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE)
    State = models.CharField(max_length=150, choices=STATECHOICE, default='draft')
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)

@receiver(post_save, sender=Cart)
def set_addressId(sender, instance, created, **kwargs):
    if created:
        instance.CartId = to_roman_numeral(instance.id)
        instance.save()


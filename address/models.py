from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop import  to_roman_numeral
from Users.models import User


class City(models.Model):

    CityId = models.CharField(max_length=50, unique=True)
    Name = models.CharField(max_length=50)
    Parents = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)


class Address(models.Model):

    AddressId = models.CharField(max_length=50, unique=True)
    Title = models.CharField(max_length=50)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    City = models.ForeignKey(City, on_delete=models.CASCADE)
    # Province = models.ForeignKey(City, on_delete=models.CASCADE)
    AddressTxt = models.TextField()
    ReceiverName = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=20)
    PostalCode = models.CharField(max_length=15)


@receiver(post_save, sender=Address)
def set_addressId(sender, instance, created, **kwargs):
    if created:
        instance.AddressId = to_roman_numeral(instance.id)
        instance.save()

@receiver(post_save, sender=City)
def set_cityId(sender, instance, created, **kwargs):
    if created:
        instance.CityId = to_roman_numeral(instance.id)
        instance.save()



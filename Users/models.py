from django.db import models
from django.contrib.auth.models import  AbstractUser
from  django_otp.models import Device

from Users.manager import MyUserManager

class Rols(models.Model):

    RoleId = models.CharField(max_length=150,unique=True)
    Title = models.CharField(max_length=250)


STATECHOICE = (
    ('nv', 'not_validated')
    ,('v', 'validated')
)
class User (AbstractUser):
    username = models.CharField(null=True, max_length=15)
    RoleId = models.ForeignKey(Rols, on_delete=models.CASCADE, null=True)
    PhoneNumber = models.CharField(max_length=14)
    Address = models.TextField()
    state = models.CharField(max_length=15, choices=STATECHOICE)
    Birthday = models.DateField(null=True, default=None)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', ]

    objects = MyUserManager()

    def __str__(self):
        return  self.PhoneNumber


class OTPDevice(Device):
    pass





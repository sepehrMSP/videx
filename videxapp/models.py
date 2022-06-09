from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class VidexUser(AbstractUser):
    national_id = models.IntegerField(null=True, blank=True, verbose_name="کد ملی")
    telephone_number = models.CharField(null=True, max_length=11, verbose_name='cellphone number')
    balance = models.IntegerField(verbose_name='balance', default=0)
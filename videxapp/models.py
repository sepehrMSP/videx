from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class VidexUser(AbstractUser):
    national_id = models.IntegerField(null=True, blank=True, verbose_name="کد ملی")

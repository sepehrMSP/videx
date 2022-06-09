from django.contrib import admin

from videxapp.models import Course, VidexUser

# Register your models here.

admin.site.register(VidexUser)
admin.site.register(Course)
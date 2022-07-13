from django.contrib import admin

from videxapp.models import *

# Register your models here.

admin.site.register(VidexUser)
admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Exam)
admin.site.register(Answer)


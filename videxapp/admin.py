from django.contrib import admin

from videxapp.models import Chatroom, Comment, Course, Session, VidexUser

# Register your models here.

admin.site.register(VidexUser)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Chatroom)
admin.site.register(Session)

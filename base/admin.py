from django.contrib import admin

# Register your models here.

from .models import Topic, Room, Message, Type

admin.site.register(Topic)
admin.site.register(Type)
admin.site.register(Room)
admin.site.register(Message)
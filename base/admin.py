from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message #User model is registered by default (django built-in stuff, yaknow), so do not need to import it

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
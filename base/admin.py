from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, User #since User is modified in models, we need to import it as well

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
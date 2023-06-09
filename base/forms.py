from django.forms import ModelForm #"Kind of like a class-based representation of a form" - does some of the work for ya
from django.contrib.auth.forms import UserCreationForm 
from .models import Room, User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' # create all fields that are specified in the Room model (except for fields that aren't possible to update/change manually, eg. updated/changed)
        exclude = ['host', 'participants'] #one way to remove some fields from the form. remember to add these values in views.py so that something will be sent to the db


class UserForm(ModelForm): #form that lets user edit own info on profile
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
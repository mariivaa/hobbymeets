from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

#GENERALLY; each model maps to a single database table


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg") #TODO: fix the avatar to be something more fun, ideally a few that are randomly assigned

    USERNAME_FIELD = 'email' # override orig. User and set email as login info
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #ForeignKey establishes a parent-child relationship with Topic. Need to allow null=True in the db bc of SET_NULL 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # null=True doesn't actually do much as explained here: https://stackoverflow.com/questions/8609192/what-is-the-difference-between-null-true-and-blank-true-in-django
                                                        #blank=True -> you can leavve fields blank (not required to fill out)
    participants = models.ManyToManyField(User, related_name='participants', blank=True) #more about related_name on Notion/Stackoverflow. Blank=true means you can submit a form without filling everying out
    updated = models.DateTimeField(auto_now=True) #auto_now takes a snapshot everytime the instance is saved _ Eg. when the room was last updated
    created = models.DateTimeField(auto_now_add=True) #only takes a timestamp when the instance is created - Eg. when the room was created

    class Meta:
        ordering = ['-updated', '-created'] #the dash means descending order, eg. newest updated / created will be first
    
    def __str__(self):
        return self.name #has to be a string!! so if unsire, wrap the retunred val in a str()
        



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #the user that is posting the message. User class is imported (django.contrib.auth.models)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #ForeignKey establishes a parent-child relationship with Room, and CASCADE means that when a Room object is deleted, all its children are deleted as well
    body = models.TextField() #leave empty to force users to write message
    updated = models.DateTimeField(auto_now=True) #auto_now takes a snapshot everytime the instance is saved _ Eg. when the room was last updated
    created = models.DateTimeField(auto_now_add=True) #only takes a timestamp when the instance is created - Eg. when the room was created

    class Meta:
        ordering = ['-created'] #the dash means descending order, eg. newest updated / created will be first

    def __str__(self):
        return self.body[0:50] #gives you a preview of the first 50 characters
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages #django flash messages (one-time notification messages)
from django.contrib.auth.decorators import login_required #needed to restrict pages to authorized users
from django.db.models import Q #lets you add AND/OR statements into the search criteria
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm 
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm
'''
REQUESTS explained: When a page is requested, Django creates an HttpRequest object that contains metadata about the request. 
Then Django loads the appropriate view, passing the HttpRequest as the first argument to the view function. 
Each view is responsible for returning an HttpResponse object. -django docs
'''

'''
rooms = [
    {'id':1, 'name':'Lets learn this stufff'},
    {'id':2, 'name':'SQL study room'},
    {'id':3, 'name':'DP-900 exam prep'},
] 
'''


def loginPage(request): #don't cann this function 'login' if you plan to use the built in login() function (to avoid conflict)
    page = 'login'

    #check if user is already logged in:
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #to make sure the user exists:
        try:
            user = User.objects.get(username=username)
        except:
            #use django one-time notification message:
            messages.error(request, 'User does not exist. Try different credentials or create a new user.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) #creates a session in the DB and the browser(cookies)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request) #use Django logout function to fix all the stuff for you (wrt session etc.)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST) #param request.POST means passing in all credentials such as name, password, etc.
        if form.is_valid():
            user = form.save(commit=False) #need to set commit=False in order to access the user object
            user.username = user.username.lower() #clean
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error ocurred during registration.')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' #q for query hehe. q returns whatever is passed into the url. youtube: 2:13:40 for more
    
    rooms = Room.objects.filter( #filter() w/out parameters works just like all()
        Q(topic__name__icontains=q) | #icontains is for the search functionality, makes it possible to search for partial matches (i makes it case insensitive)
        Q(name__icontains=q) | #topic__name, name, description are all keywords of filter, not of Room model. topic__name is a composite keyword that goes into the parent function   
        Q(description__icontains=q)
        )  
    topics = Topic.objects.all()[0:5] #TODO: fix this so that the most popular topics appear first?
    room_count = rooms.count() #faster than len() method
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
                'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk) #the get function looks in the Room model(db) for an id that matches pk. Each model object in Django gets an id autmatically assigned. 
    room_messages = room.message_set.all() #since Message model has Room as FK, you can access the Message objects from the related Room through message_set.
    participants = room.participants.all() #can use participants.all() bc participants has been specified as a related_name in models.

    #add functionality to post a message in a room:
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user) #adds participant to room when they post something (every single time...?)
        return redirect('room', pk=room.id)
    context = {'room' : room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() #_set gets relevant rooms through reverse relation from user intance
    room_messages = user.message_set.all()
    topics =  Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login') #redirects unauthorized users to the login page
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST': 
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
        host=request.user,
        topic=topic,
        name=request.POST.get('name'), #name passed from the form (form.name)
        description=request.POST.get('description')#passed from the form
        )
        return redirect('home') #redirects user to homepage after submitting form
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login') #checks if authorized and redirects unauthorized users to the login page
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    #give feedback to unauthorized users:
    if request.user != room.host:
        return HttpResponse('Få dæ vækk ditt håratt spøkels, du e itj vælkommen hær!')

    if request.method == 'POST': #follow same principle for this if clause as in createRoom()
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login') #redirects unauthorized users to the login page
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)


    #give feedback to unauthorized users:
    if request.user != room.host:
        return HttpResponse('Få dæ vækk ditt håratt spøkels, du får itj slætta dt hær!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj' : room}) #'obj' refers to the 'obj in delete.html


@login_required(login_url='login') 
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    #give feedback to unauthorized users:
    if request.user != message.user:
        return HttpResponse('Få dæ vækk ditt håratt spøkels, du får itj slætta dt hær!')

    if request.method == 'POST':
        message.delete()
        return redirect('home') #TODO: send users back to prev page
    return render(request, 'base/delete.html', {'obj' : message})



@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update_user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics  =Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
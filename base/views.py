from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages #django flash messages (one-time notification messages)
from django.contrib.auth.decorators import login_required #needed to restrict pages to authorized users
from django.db.models import Q #lets you add AND/OR statements into the search criteria
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm 
from .models import Room, Topic
from .forms import RoomForm
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
    q = request.GET.get('q') if request.GET.get('q') != None else '' #q for query hehe. q returs whatever is passed into the url. youtube: 2:13:40 for more
    
    rooms = Room.objects.filter( #filter() w/out parameters works just like all()
        Q(topic__name__icontains=q) | #icontains is for the search functionality, makes it possible to search for partial matches (i makes it case insensitive)
        Q(name__icontains=q) | #topic__name, name, description are all keywords of filter, not of Room model. topic__name is a composite keyword that goes into the parent function   
        Q(description__icontains=q)
        )  

    topics = Topic.objects.all()
    room_count = rooms.count() #faster than len() method

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk) #the get function looks in the Room model(db) for an id that matches pk. Each model object in Django gets an id autmatically assigned. 
    context = {'room' : room}
    return render(request, 'base/room.html', context)


@login_required(login_url='login') #redirects unauthorized users to the login page
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST': 
        form = RoomForm(request.POST) # since we use ModelForm for RoomForm (in .forms), we can just pass in all the POST data into the form, and it will know which values to extract
        if form.is_valid():
            form.save()
            return redirect('home') #redirects user to homepage after submitting form
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login') #redirects unauthorized users to the login page
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    #give feedback to unauthorized users:
    if request.user != room.host:
        return HttpResponse('Få dæ vækk ditt håratt spøkels, du e itj vælkommen hær!')

    if request.method == 'POST': #follow same principle for this if clause as in createRoom()
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
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
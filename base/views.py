from django.shortcuts import render, redirect
from .models import Room
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

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk) #the get function looks in the Room model(db) for an id that matches pk. Each model object in Django gets an id autmatically assigned. 
    context = {'room' : room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST': 
        form = RoomForm(request.POST) # since we use ModelForm for RoomForm (in .forms), we can just pass in all the POST data into the form, and it will know which values to extract
        if form.is_valid():
            form.save()
            return redirect('home') #redirects user to homepage after submitting form
    context = {'form': form}
    return render(request, 'base/room_form.html', context)
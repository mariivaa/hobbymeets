from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"), #three parameters: home page path, home view from the views file, and an optional name to call this view/url (handy bc you can reference the url by its name in other files. Then, if the url changes you only need to update it in this file)
    path('room/<str:pk>', views.room, name = "room"), #c <> is used to make whatever you pass in dynamic (in our case a string), and pk stands for primary key 

    path('create-room/', views.createRoom, name="create-room"),

]
from django.urls import path
from . import views

'''
path('example/', views.example_function, name="example_name") basically says:
“When someone navigates to http://www.hobbyrooms.com/example/, 
run the example_function() inside the views.py file”.

'''

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name ="home"), #three parameters: home page path, home view from the views file, and an optional name to call this view/url (handy bc you can reference the url by its name in other files. Then, if the url changes you only need to update it in this file)
    path('room/<str:pk>', views.room, name ="room"), #c <> is used to make whatever you pass in dynamic (in our case a string), and pk stands for primary key 
    path('profile/<str:pk>/', views.userProfile, name ="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
]
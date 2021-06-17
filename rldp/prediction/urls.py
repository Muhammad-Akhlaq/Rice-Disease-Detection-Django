from django.contrib import admin
from django.urls import path, include
from prediction import views

urlpatterns = [
    path('', views.home, name='home'),
    path('result/', views.result, name='result'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
]

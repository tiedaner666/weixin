from django.urls import path
from login import views


urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('index/', views.index),

]


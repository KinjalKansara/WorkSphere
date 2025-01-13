from django.urls import path
from . import views

urlpatterns = [
    path('client_chatbox/', views.client_chatbox, name='client_chatbox'),
    path('freelancer_chatbox/', views.freelancer_chatbox, name='freelancer_chatbox'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('rating/', views.rating, name='rating'),
]
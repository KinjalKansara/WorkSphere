from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('help/', views.help, name='help'),
    path('service/', views.service, name='service'),
    path('home/', views.home, name='home'),
    path('work/', views.work, name='work'),
    path('select_register/', views.select_register, name='select_register'),
    path('select_login/', views.select_login, name='select_login'),
    path('terms/', views.terms, name='terms'),
    path('policy/', views.policy, name='policy'),
    path('header_footer/', views.header_footer, name='header_footer'),
    path('header_footer_select/', views.header_footer_select, name='header_footer_select'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_contact/', views.admin_contact, name='admin_contact'),
    path('admin_client/', views.admin_client, name='admin_client'),
    path('admin_freelancer/', views.admin_freelancer, name='admin_freelancer'),
    path('admin_payment/', views.admin_payment, name='admin_payment'),
    path('admin_project/', views.admin_project, name='admin_project'),
    path('admin_proposal/', views.admin_proposal, name='admin_proposal'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_forgot_password/', views.admin_forgot_password, name='admin_forgot_password'),
    path('admin_verify_otp/', views.admin_verify_otp, name='admin_verify_otp'),
    path('admin_reset_password/', views.admin_reset_password, name='admin_reset_password'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
]
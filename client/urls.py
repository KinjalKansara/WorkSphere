from django.urls import path
from . import views

urlpatterns = [
    path('client_forgot_password/', views.client_forgot_password, name='client_forgot_password'),
    path('client_reset_password/', views.client_reset_password, name='client_reset_password'),
    path('client_register_login/', views.client_register_login, name='client_register_login'),
    path('client_verify_otp/', views.client_verify_otp, name='client_verify_otp'),
    path('client_contact/', views.client_contact, name='client_contact'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client_post_project/', views.client_post_project, name='client_post_project'),
    path('client_freelancer_profile/', views.client_freelancer_profile, name='client_freelancer_profile'),
    # path('client_job_details/', views.client_job_details, name='client_job_details'),
    path('client_job_details/<int:project_id>/', views.client_job_details, name='client_job_details'),
    path('client_list_of_project/', views.client_list_of_project, name='client_list_of_project'),
    path('client_profile/', views.client_profile, name='client_profile'),
    path('client_edit_profile/', views.client_edit_profile, name='client_edit_profile'),
    path('client_received_proposal/', views.client_received_proposal, name='client_received_proposal'),
    path('header_1/', views.header_1, name='header_1'),
    path('header_2/', views.header_2, name='header_2'),
    path('header_3/', views.header_3, name='header_3'),
    path('client_logout/', views.client_logout, name='client_logout'),

    
]
from django.urls import path
from . import views

urlpatterns = [
    path('freelancer_register_login/', views.freelancer_register_login, name='freelancer_register_login'),
    path('freelancer_forgot_password/', views.freelancer_forgot_password, name='freelancer_forgot_password'),
    path('freelancer_reset_password/', views.freelancer_reset_password, name='freelancer_reset_password'),
    path('freelancer_verify_otp/', views.freelancer_verify_otp, name='freelancer_verify_otp'),
    path('freelancer_dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('freelancer_contact/', views.freelancer_contact, name='freelancer_contact'),
    path('freelancer_job_details/<int:project_id>', views.freelancer_job_details, name='freelancer_job_details'),
    path('freelancer_list_of_project/', views.freelancer_list_of_project, name='freelancer_list_of_project'),
    path('freelancer_profile/', views.freelancer_profile, name='freelancer_profile'),
    path('freelancer_edit_profile/', views.freelancer_edit_profile, name='freelancer_edit_profile'),
    path('freelancer_proposal/', views.freelancer_proposal, name='freelancer_proposal'),
    path('freelancer_send_proposal/', views.freelancer_send_proposal, name='freelancer_send_proposal'),
    path('freelancer_header_1/', views.freelancer_header_1, name='freelancer_header_1'),
    path('freelancer_header_2/', views.freelancer_header_2, name='freelancer_header_2'),
    path('freelancer_header_3/', views.freelancer_header_3, name='freelancer_header_3'),
    path('logout/', views.logout, name='logout'),
]
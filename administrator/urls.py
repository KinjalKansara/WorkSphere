from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('send-email/', views.send_email, name='send_email'),
    path('admin_contact/', views.admin_contact, name='admin_contact'),
    path('admin_delete_contact/<int:id>', views.admin_delete_contact, name='admin_delete_contact'),
    path('admin_client/', views.admin_client, name='admin_client'),
    path('admin_delete_client/<int:id>', views.admin_delete_client, name='admin_delete_client'),
    path('admin_freelancer/', views.admin_freelancer, name='admin_freelancer'),
    path('freelancer_delete_details/<int:id>/', views.freelancer_delete_details, name='freelancer_delete_details'),
    path('admin_payment/', views.admin_payment, name='admin_payment'),
    path('admin_project/', views.admin_project, name='admin_project'),
    path('admin_delete_project/<int:id>', views.admin_delete_project, name='admin_delete_project'),
    path('admin_proposal/', views.admin_proposal, name='admin_proposal'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_forgot_password/', views.admin_forgot_password, name='admin_forgot_password'),
    path('admin_verify_otp/', views.admin_verify_otp, name='admin_verify_otp'),
    path('admin_reset_password/', views.admin_reset_password, name='admin_reset_password'),
    path('admin_header_1/', views.admin_header_1, name='admin_header_1'),
    path('admin_header_2/', views.admin_header_2, name='admin_header_2'),
    path('admin_header_3/', views.admin_header_3, name='admin_header_3'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin/payment/update/<int:payment_id>/', views.update_project_status, name='update_project_status'),
    path('admin/payment/delete/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path("generate_report/", views.generate_report, name="generate_report"),
    path("generate_pdf/", views.generate_pdf, name="generate_pdf"),
]
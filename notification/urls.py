from django.urls import path
from . import views

urlpatterns = [
    path('post_project/', views.post_project, name='post_project'),
    path('submit_proposal/<int:project_id>/', views.submit_proposal, name='submit_proposal'),
    path('approve_proposal/<int:proposal_id>/', views.approve_proposal, name='approve_proposal'),
    path('submit_project/<int:project_id>/', views.submit_project, name='submit_project'),
    path('client_register/', views.client_register, name='client_register'),
    path('freelancer_register/', views.freelancer_register, name='freelancer_register'),
    path('send_contact_message/', views.send_contact_message, name='send_contact_message'),
    path('payment_received/<int:payment_id>/', views.payment_received, name='payment_received'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]

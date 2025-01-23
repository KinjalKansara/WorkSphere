from django.db import models
from django.db import models
from administrator.models import AdminUser

# Create your models here.



class Notification(models.Model):
    MESSAGE_TYPES = [
        ('project_posted', 'Project Posted'),
        ('proposal_submitted', 'Proposal Submitted'),
        ('proposal_approved', 'Proposal Approved'),
        ('submission_received', 'Submission Received'),
        ('project_submitted', 'Project Submitted'),
        ('client_registered', 'Client Registered'),
        ('freelancer_registered', 'Freelancer Registered'),
        ('contact_message', 'Contact Message'),
        ('payment_received', 'Payment Received'),
    ]
    
    user = models.ForeignKey(AdminUser, on_delete=models.CASCADE)  # User receiving the notification
    message_type = models.CharField(max_length=50, choices=MESSAGE_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.username} - {self.message_type}"

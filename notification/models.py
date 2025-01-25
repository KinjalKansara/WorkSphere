from django.db import models
from django.db import models
from administrator.models import AdminUser

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    ]
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    # user = models.ForeignKey(AdminUser, on_delete=models.CASCADE)  # The user receiving the notification
    notification_type = models.CharField(choices=NOTIFICATION_TYPES, max_length=50)
    username = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.db import models

# Create your models here.

class ClientContact(models.Model):
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the contact was submitted

    def __str__(self):
        return f"Contact from {self.email}"
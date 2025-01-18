from django.db import models

from client.models import ClientPostProject

# Create your models here.

class FreelancerRegisterLogin(models.Model):
    profile = models.ImageField(upload_to='profile_images/')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    skills = models.CharField(max_length=50)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    location = models.CharField(max_length=100)
    about_me = models.TextField(null=True, max_length=1000)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'
    

class FreelancerProposal(models.Model):
    DURATION_CHOICES = [
        ('1_day', '1 Day'),
        ('2_days', '2 Days'),
        ('3_days', '3 Days'),
        ('4_days', '4 Days'),
        ('5_days', '5 Days'),
        ('7_days', '7 Days'),
        ('10_days', '10 Days'),
        ('15_days', '15 Days'),
        ('1_month', '1 Month'),
        ('2_months', '2 Months'),
        ('3_months', '3 Months'),
    ]

    freelancer = models.ForeignKey(FreelancerRegisterLogin, on_delete=models.CASCADE)
    project = models.ForeignKey(ClientPostProject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(editable=False)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    cover_letter = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"Proposal by {self.freelancer.username} for project: {self.project_title}"


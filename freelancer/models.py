from django.db import models

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
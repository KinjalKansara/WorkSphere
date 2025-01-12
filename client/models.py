from django.db import models


class ClientRegisterLogin(models.Model):
    profile_photo = models.ImageField(upload_to='profile_photos/')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    company = models.CharField(max_length=100)
    bio = models.TextField(null=True, max_length=1000)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
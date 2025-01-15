from django.db import models

class AdminUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email


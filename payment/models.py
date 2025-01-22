from django.db import models

from client.models import ClientPostProject
from freelancer.models import *

# Create your models here.

class Payment(models.Model):
    proposal = models.ForeignKey(FreelancerProposal, on_delete=models.CASCADE, related_name='payments', null=True)
    order_id = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=50)
    signature = models.CharField(max_length=256, null=True, blank=True)
    refund_payment_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    email = models.EmailField()  # Added field to store the user's email
    status = models.CharField(max_length=100, choices=[(
        'Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')

    def __str__(self):
        return f"Payment - {self.order_id} for {self.email}"
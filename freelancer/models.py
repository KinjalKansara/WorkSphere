from django.db import models

from client.models import ClientPostProject, ClientRegisterLogin

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
    hourly_rate = models.DecimalField(max_digits=20, decimal_places=2)
    location = models.CharField(max_length=100)
    about_me = models.TextField(null=True, max_length=1000)

    bank_name = models.CharField(max_length=50, null=True, blank=True)  # Bank name
    ifsc_code = models.CharField(max_length=20, null=True, blank=True)  # IFSC code
    account_number = models.CharField(max_length=20, null=True, blank=True)  # Account number

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
    client = models.ForeignKey(ClientRegisterLogin, on_delete=models.CASCADE, null=True)
    freelancer = models.ForeignKey(FreelancerRegisterLogin, on_delete=models.CASCADE)
    project = models.ForeignKey(ClientPostProject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(editable=False)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    bid = models.DecimalField(max_digits=10, decimal_places=2)  # Default bid value
    cover_letter = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"Proposal by {self.freelancer.username} for project: {self.project.title}"
    
class ProjectPayments(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
    ]
    proposal = models.ForeignKey(FreelancerProposal, on_delete=models.CASCADE)
    project_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField( max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Unpaid')





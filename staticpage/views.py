from django.shortcuts import render
from django.core.mail import send_mail
import re

from client.models import ClientPostProject, ClientRegisterLogin
from freelancer.models import FreelancerProposal, FreelancerRegisterLogin
from .models import *

# Create your views here.

def header_footer(request):
    return render(request, 'header_footer.html')

def home(request):
    stats = {
        'total_clients': ClientRegisterLogin.objects.count(),
        'total_freelancers': FreelancerRegisterLogin.objects.count(),
        'total_proposals': FreelancerProposal.objects.count(),
        'total_projects': ClientPostProject.objects.count(),
    }
    return render(request, 'home.html', {'stats': stats})

def terms(request):
    return render(request, 'terms.html')

def work(request):
    return render(request, 'how_it_work.html')

def policy(request):
    return render(request, 'policy.html')

def help(request):
    return render(request, 'help_center.html')

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def contact(request):
    if request.method == 'POST':
        first = request.POST.get('firstname')
        last = request.POST.get('lastname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        phone_number = request.POST.get('phonenumber')

        errors_message = None  # Initialize error message variable

        # Validate first name
        if not first:
            errors_message = 'First name is required.'
        elif len(first) < 2:
            errors_message = 'First name must be at least 2 characters.'

        # Validate last name
        if not last:
            errors_message = 'Last name is required.'
        elif len(last) < 2:
            errors_message = 'Last name must be at least 2 characters.'

        # Validate email using regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email:
            errors_message = 'Email is required.'
        elif not re.match(email_regex, email):
            errors_message = 'Enter a valid email address.'

        # Validate phone number using regex
        phone_regex = r'^\d{10}$'
        if not phone_number:
            errors_message = 'Phone number is required.'
        elif not re.match(phone_regex, phone_number):
            errors_message = 'Phone number must be exactly 10 digits.'

        # Validate subject
        if not subject:
            errors_message = 'Subject is required.'

        # Validate message
        if not message:
            errors_message = 'Message is required.'

        # If there is any error, render the page with the error message
        if errors_message:
            return render(request, 'contact.html', {'error_message': errors_message})
        

        contact = ClientContact(
            first=first, 
            last=last, 
            email=email, 
            subject=subject, 
            message=message, 
            phone_number=phone_number
        )

        try:
            contact.save()
            # Send email to admin
            send_mail(
                subject=f'New Contact Form Submission: {subject}',
                message=f'You have a new contact form submission.\n\n'
                        f'Name: {first} {last}\n'
                        f'Email: {email}\n'
                        f'Phone: {phone_number}\n\n'
                        f'Message:\n{message}',
                from_email=email,
                recipient_list=['worksphere05@gmail.com'],  # Replace with your admin email
                fail_silently=False,
            )
            return render(request, 'home.html')
        except:
            return render(request, 'contact.html', {'error': 'Failed to save contact information.'})
    return render(request, 'contact.html')  

def categories(request):
    return render(request, 'categories.html')

def select_register(request):
    return render(request, 'select_register.html')

def select_login(request):
    return render(request, 'select_login.html')

def header_footer_select(request):
    return render(request, 'header_footer_select.html')


def error_404_view(request, exception=None):
    return render(request, '404.html', status=404)
from django.shortcuts import render, redirect
from .models import *
from staticpage.models import *
import random
import re
from django.core.mail import send_mail

# Create your views here.


def freelancer_register_login(request):
    if request.method == 'POST':
        profile = request.FILES.get('profile')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phonenumber = request.POST.get('phonenumber')
        skill = request.POST.get('skill')
        hourlyrate = request.POST.get('horlyrate')
        location = request.POST.get('location')
        

        register = FreelancerRegisterLogin(
            profile=profile,
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password,
            phone_number=phonenumber,
            skills = skill,
            hourly_rate = hourlyrate,
            location = location
        )

        try:
            register.save()
            return redirect('freelancer_dashboard')
        except:
            return render(request, 'auth/freelancer_register_login.html', {'error': 'Failed to save registration information.'})
    return render(request, 'auth/freelancer_register_login.html')

def freelancer_forgot_password(request):
    return render(request, 'auth/freelancer_forgot_password.html')

def freelancer_verify_otp(request):
    return render(request, 'auth/freelancer_verify_otp.html')

def freelancer_reset_password(request):
    return render(request, 'auth/freelancer_reset_password.html')



def freelancer_contact(request):
    if request.method == 'POST':
        first = request.POST.get('firstname')
        last = request.POST.get('lastname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        phone_number = request.POST.get('phonenumber')

        #validation

        errors = {}

        if not first:
            errors['firstname'] = 'First name is required.'
        elif len(first) < 2:
            errors['firstname'] = 'First name must be at least 2 characters.'

        # Validate last name
        if not last:
            errors['lastname'] = 'Last name is required.'
        elif len(last) < 2:
            errors['lastname'] = 'Last name must be at least 2 characters.'

        # Validate email using regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email:
            errors['email'] = 'Email is required.'
        elif not re.match(email_regex, email):
            errors['email'] = 'Enter a valid email address.'

        # Validate phone number using regex
        phone_regex = r'^\d{10}$'
        if not phone_number:
            errors['phonenumber'] = 'Phone number is required.'
        elif not re.match(phone_regex, phone_number):
            errors['phonenumber'] = 'Phone number must be exactly 10 digits.'

        # Validate subject
        if not subject:
            errors['subject'] = 'Subject is required.'

        # Validate message
        if not message:
            errors['message'] = 'Message is required.'

        if errors:
            return render(request, 'client_contact.html', {'errors': errors})
        

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
            return redirect("freelancer_dashboard")
        except:
            return render(request, 'freelancer_contact.html', {'error': 'Failed to save contact information.'})
    return render(request, 'freelancer_contact.html') 


def freelancer_dashboard(request):
    return render(request, 'freelancer_dashboard.html')


def freelancer_job_details(request):
    return render(request, 'freelancer_job_details.html')


def freelancer_list_of_project(request):
    return render(request, 'freelancer_list_of_project.html')

def freelancer_profile(request):
    return render(request, 'freelancer_profile.html')

def freelancer_edit_profile(request):
    return render(request, 'freelancer_edit_profile.html')

def freelancer_proposal(request):
    return render(request, 'freelancer_proposal.html')

def freelancer_send_proposal(request):
    return render(request, 'freelancer_send_proposal.html')
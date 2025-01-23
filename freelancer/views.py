import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from WorkSphere import settings
from payment.models import Payment
from .models import *
from staticpage.models import *
from client.models import *
import random
import re
from django.core.mail import send_mail

# Create your views here.

from django.core.mail import send_mail
from django.conf import settings
import re

def freelancer_register_login(request):
    if 'done' in request.GET:
        del request.session['done']

    if request.method == 'POST':
        profile = request.FILES.get('profile')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phonenumber = request.POST.get('phonenumber')
        skill = request.POST.get('skill')
        hourlyrate = request.POST.get('hourlyrate')
        location = request.POST.get('location')
        login = request.POST.get('login')

        print(profile,firstname,lastname,username,email, password,phonenumber,skill,hourlyrate,location)

        if login is not None:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username:
                error_messages = "User Name is Required"

            if not password:
                error_messages = "Password is Required"

            try:
                user = FreelancerRegisterLogin.objects.get(username=username, password=password)
                request.session['logged_user'] = username
                request.session['role'] = 'FREELANCER'
                request.session['show_modal'] = True
                return redirect('freelancer_dashboard')
            except FreelancerRegisterLogin.DoesNotExist:
                error_messages = 'Invalid username or password.'
                return render(request, 'auth/freelancer_register_login.html', {'error_messages': error_messages})

        else:
            # Validation
            error_message = None  # Ensure error_message is initialized here
            if not profile:
                error_message = 'Profile photo is required.'
            elif not firstname:
                error_message = 'First name is required.'
            elif not lastname:
                error_message = 'Last name is required.'
            elif not username:
                error_message = 'Username is required.'
            elif FreelancerRegisterLogin.objects.filter(username=username).exists():
                error_message = 'Username already exists.'
            else:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not email:
                    error_message = 'Email is required.'
                elif not re.match(email_regex, email):
                    error_message = 'Enter a valid email address.'
                elif FreelancerRegisterLogin.objects.filter(email=email).exists():
                    error_message = 'Email already exists.'
                elif not password:
                    error_message = "Password is Required"
                elif len(password) < 8:
                    error_message = "The password must be at least 8 characters long."
                elif not any(char.isalpha() for char in password):
                    error_message = "The password must contain at least one letter."
                elif not any(char.isdigit() for char in password):
                    error_message = "The password must contain at least one digit."
                elif not any(char in "!@#$%^&*(){}[]" for char in password):
                    error_message = "The password must contain at least one special character."
                else:
                    phone_regex = r'^\d{10}$'
                    if not phonenumber:
                        error_message = 'Phone number is required.'
                    elif not re.match(phone_regex, phonenumber):
                        error_message = 'Phone number must be exactly 10 digits.'
                    if not skill:
                        error_message = 'Skill is required.'
                    if not hourlyrate:
                        error_message = 'Hourly rate is required.'
                    elif not hourlyrate.isdigit():
                        error_message = 'Hourly rate must be a number.'

            if error_message:
                return render(request, 'auth/freelancer_register_login.html', {'error_message': error_message})

            # Save FreelancerRegisterLogin
            register = FreelancerRegisterLogin(
                profile=profile,
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=password,
                phone_number=phonenumber,
                skills=skill,
                hourly_rate=hourlyrate,
                location=location
            )

            try:
                register.save()
                send_mail(
                    subject="Welcome to WorksPhere!",
                    message=f"Dear {firstname},\n\nThank you for registering with WorksPhere as a client. Your account is now active, and you can log in to start posting projects and finding freelancers.\n\nBest regards,\nWorksPhere Team",
                    from_email='worksphere05@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                )
                request.session['done'] = True
                return render(request, 'auth/freelancer_register_login.html', {'success': 'Registration successful.', 'done': request.session['done']})
            except Exception as e:
                request.session['done'] = False
                error_message = 'Registration failed. Please try again.'

            return render(request, 'auth/freelancer_register_login.html', {'error_message': error_message})

    return render(request, 'auth/freelancer_register_login.html')


def freelancer_forgot_password(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')

        if not user_email:
            error_message = "Email is required."
        # Validation: Check if email is valid
        elif '@' not in user_email:
            error_message = "Enter a valid email."

        else:
            try:
                user = FreelancerRegisterLogin.objects.get(email=user_email)
        
                otp = random.randint(100000,999999)
                request.session['otp'] = otp
                request.session['email'] = user.email

                send_mail(
                    subject='Password Reset',
                    message=f'Your OTP is {otp}',
                    from_email='worksphere05@gmail.com',  # Replace with your sender email
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                return redirect('freelancer_verify_otp')
            except FreelancerRegisterLogin.DoesNotExist:
                error_message = "Email does not exist in our records."
    
    return render(request, 'auth/freelancer_forgot_password.html', {'error_message': error_message})

def freelancer_verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        if not otp:
            error_message = "OTP is required."
        elif not otp.isdigit() or len(otp) != 6:
            error_message = "Please enter a valid 6-digit OTP."
        elif int(otp) != request.session.get('otp'):
            # Check if the entered OTP matches the one stored in the session
            error_message = "Invalid OTP. Please try again."
        else:
            return redirect('client_reset_password')
        
        return render(request, 'auth/freelancer_verify_otp.html', {'error_message': error_message})
        
    return render(request, 'auth/freelancer_verify_otp.html')

def freelancer_reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password Validation
        if not password:
            error_message = 'Password is required.'
        elif len(password) < 8:
            error_message = 'The password must be at least 8 characters long.'
        elif not any(char.isalpha() for char in password):
            error_message = 'The password must contain at least one letter.'
        elif not any(char.isdigit() for char in password):
            error_message = 'The password must contain at least one digit.'
        elif not any(char in "!@#$%^&*(){}[]" for char in password):
            error_message = 'The password must contain at least one special character.'
        elif password != confirm_password:
            error_message = 'Password and confirm password do not match.'

        # If there is any validation error, show the error message
        if error_message:
            return render(request, 'auth/client_reset_password.html', {'error_message': error_message})

        else:
            user_email = request.session.get('email')
            user = ClientRegisterLogin.objects.get(email=user_email)
            user.password = password  # Set the new password
            user.save()  # Save the updated user object
            request.session.flush()  # Clear the session
            request.session['done'] = True  # Set a flag indicating successful reset
            return redirect('freelancer_register_login')  # Redirect to login page

    return render(request, 'auth/freelancer_reset_password.html')

def freelancer_contact(request):
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
            return render(request, 'freelancer_contact.html', {'error_message': errors_message})

        # If no errors, save contact information and send email
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
        except Exception as e:
            return render(request, 'freelancer_contact.html', {'error': f'Failed to save contact information: {str(e)}'})

    return render(request, 'freelancer_contact.html')


def freelancer_dashboard(request):
    return render(request, 'freelancer_dashboard.html')

def freelancer_job_details(request, project_id):
    username = request.session.get('logged_user')
    freelancer = FreelancerRegisterLogin.objects.get(username = username)
    details = ClientPostProject.objects.get(id=project_id)
    proposal = FreelancerProposal.objects.filter(freelancer=freelancer, project=details).first()
    payment = Payment.objects.filter(proposal=proposal).first()
    skills = details.skills_required.split(',')  # Assuming skills are stored as a comma-separated string
    deadline = details.deadline
    today = datetime.date.today()
    context = {
        'details' : details,
        'skills' : skills,
        'freelancer' : freelancer,
        'today' : today,
        'deadline' : deadline,
        'payment' : payment,
    }
    return render(request, 'freelancer_job_details.html', context)

def freelancer_list_of_project(request):
    # proposal = FreelancerProposal.objects.filter()
    projects = ClientPostProject.objects.filter(status = 'open')

    context={
        'projects' : projects,
        # 'proposal' : proposal,
        'details': {'description': 'Your project description <br> with <strong>HTML</strong> formatting here.'}, # Replace with actual project details
    }
    return render(request, 'freelancer_list_of_project.html', context)

def freelancer_profile(request):
    username = request.session.get('logged_user')
    freelancer = FreelancerRegisterLogin.objects.get(username=username)

    context ={
        'freelancer' : freelancer,
    }
    
    return render(request, 'freelancer_profile.html', context)

def freelancer_edit_profile(request):
    username = request.session.get('logged_user')
    freelancer = FreelancerRegisterLogin.objects.get(username=username)

    if request.method == "POST":
        about = request.POST.get('about')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        skill = request.POST.get('skill')
        rate = request.POST.get('rate')

        if about:
            freelancer.about_me = about 
        if password:
            freelancer.password = password
        if phone:
            freelancer.phone_number = phone
        if location:
            freelancer.location = location
        if skill:
            freelancer.skills = skill
        if rate:
            freelancer.hourly_rate = Decimal(rate)

        freelancer.save()

        return redirect('freelancer_profile')

    context = {
        'freelancer': freelancer,
    }

    return render(request, 'freelancer_edit_profile.html', context)

def confirm_proposal(request):
    user = request.session.get('logged_user')  # Get the logged-in user's session
    freelancer = FreelancerRegisterLogin.objects.get(username=user)
    
    # Fetching proposals related to the freelancer
    proposals = Payment.objects.filter(proposal__freelancer=freelancer)

    context = {
        'proposals': proposals  # Change variable name for clarity
    }

    return render(request, 'confirm_proposal.html', context)


def freelancer_proposal(request):
    user = request.session.get('logged_user')  # Get the logged-in user's session
    freelancer = FreelancerRegisterLogin.objects.get(username=user)
    proposals = FreelancerProposal.objects.filter(freelancer=freelancer)

    context={
        'proposal' : proposals,
    }
    return render(request, 'freelancer_proposal.html', context)

def freelancer_send_proposal(request, project_id):
    user = request.session.get('logged_user')  # Get the logged-in user's session
    freelancer = FreelancerRegisterLogin.objects.get(username=user)  # Get the freelancer object
    project = ClientPostProject.objects.get(id=project_id)

    context = {
        'project': project,
    }

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        bid = request.POST.get('bid')
        if bid:
            bid = float(bid)
            service_fee = round(bid * 0.10, 2)  # 10% service fee calculation
            you_receive = round(bid - service_fee, 2)  # Amount freelancer will receive
        else:
            service_fee = 0.00
            you_receive = 0.00 # Amount freelancer will receive
        cover_letter = request.POST.get('cover_letter')
        attachment = request.FILES.get('attachment')

        # Create a FreelancerProposal object and associate it with the logged-in freelancer
        proposal = FreelancerProposal(
            freelancer=freelancer,  # Set freelancer as the logged-in freelancer
            project=project,  # Set project as the selected project
            title=title,
            description=description,
            duration=duration,
            bid=bid,
            cover_letter=cover_letter,
            attachment=attachment,
        )
        try:
            proposal.save()
            return redirect('freelancer_proposal')
        except Exception as e:
            print(e)

    return render(request, 'freelancer_send_proposal.html', context)


def freelancer_header_1(request):
    return render(request, 'freelancer_header_1.html')

def freelancer_header_2(request):
    return render(request, 'freelancer_header_2.html')

def freelancer_header_3(request):
    return render(request, 'freelancer_header_3.html')

def logout(request):
    request.session.flush()
    request.session['done'] = True
    return redirect('freelancer_register_login')
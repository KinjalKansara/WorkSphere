from django.shortcuts import render, redirect
from .models import *
from staticpage.models import *
from client.models import *
import random
import re
from django.core.mail import send_mail

# Create your views here.

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

        if login is not None:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = FreelancerRegisterLogin.objects.get(username=username, password=password)

            if user:
                request.session['logged_user'] = username
                request.session['show_modal'] = True
                return redirect('freelancer_dashboard')
            else:
                return redirect('freelancer_register_login')
        
        else:

            # Validation
            errors = {}

            if not profile:
                errors['profile'] = 'Profile photo is required.'

            if not firstname:
                errors['firstname'] = 'First name is required.'

            if not lastname:
                errors['lastname'] = 'Last name is required.'

            if not username:
                errors['username'] = 'Username is required.'
            elif FreelancerRegisterLogin.objects.filter(username=username).exists():
                errors['username'] = 'Username already exists.'

            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not email:
                errors['email'] = 'Email is required.'
            elif not re.match(email_regex, email):
                errors['email'] = 'Enter a valid email address.'
            elif FreelancerRegisterLogin.objects.filter(email=email).exists():
                errors['email'] = 'Email already exists.'

            if not password:
                errors['password'] = "Password is Required"
            elif len(password) < 8:
                errors['password'] = "The password must be at least 8 characters long."
            elif not any(char.isalpha() for char in password):
                errors['password'] = "The password must contain at least one letter."
            elif not any(char.isdigit() for char in password):
                errors['password'] = "The password must contain at least one digit."
            elif not any(char in "!@#$%^&*(){}[]" for char in password):
                errors['password'] = "The password must contain at least one special character."

            phone_regex = r'^\d{10}$'
            if not phonenumber:
                errors['phonenumber'] = 'Phone number is required.'
            elif not re.match(phone_regex, phonenumber):
                errors['phonenumber'] = 'Phone number must be exactly 10 digits.'

            if not skill:
                errors['skill'] = 'Skill is required.'

            if not hourlyrate:
                errors['hourlyrate'] = 'Hourly rate is required.'
            elif not hourlyrate.isdigit():
                errors['hourlyrate'] = 'Hourly rate must be a number.'

            if not location:
                errors['location'] = 'Location is required.'

            if errors:
                return render(request, 'auth/freelancer_register_login.html', {'errors': errors})

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
                request.session['done'] = True
                return render(request, 'auth/Freelancer_register_login.html', {'success': 'Registration successful.', 'done': request.session['done']})
            except:
                return redirect('freelancer_register_login')

    return render(request, 'auth/freelancer_register_login.html')

def freelancer_forgot_password(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user = FreelancerRegisterLogin.objects.get(email=user_email)

        if user:
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
    
    return render(request, 'auth/freelancer_forgot_password.html')

def freelancer_verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        if request.session.get('otp') == int(otp):
            return redirect('freelancer_reset_password')
        else:
            return redirect('freelancer_verify_otp')
    return render(request, 'auth/freelancer_verify_otp.html')

def freelancer_reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user_email = request.session.get('email')
            user = FreelancerRegisterLogin.objects.get(email = user_email)
            user.password = password
            user.save()
            return redirect('freelancer_register_login')
        else:
            return redirect('freelancer_reset_password')

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

def freelancer_job_details(request, project_id):
    username = request.session.get('loggedin_user')
    client = ClientRegisterLogin.objects.get(username = username)
    details = ClientPostProject.objects.get(id=project_id, client=client)
    skills = details.skills_required.split(',')  # Assuming skills are stored as a comma-separated string
    
    context = {
        'details' : details,
        'skills' : skills,
    }
    return render(request, 'freelancer_job_details.html', context)

def freelancer_list_of_project(request):
    username = request.session.get('loggedin_user')
    client = ClientRegisterLogin.objects.get(username = username)
    projects = ClientPostProject.objects.filter(client=client)

    context={
        'projects' : projects
    }
    return render(request, 'freelancer_list_of_project.html', context)

def freelancer_profile(request):
    return render(request, 'freelancer_profile.html')

def freelancer_edit_profile(request):
    return render(request, 'freelancer_edit_profile.html')

def freelancer_proposal(request):
    return render(request, 'freelancer_proposal.html')

def freelancer_send_proposal(request):
    return render(request, 'freelancer_send_proposal.html')

def freelancer_header_1(request):
    return render(request, 'freelancer_header_1.html')

def freelancer_header_2(request):
    return render(request, 'freelancer_header_2.html')

def freelancer_header_3(request):
    return render(request, 'freelancer_header_3.html')

def logout(request):
    request.session.flush()
    request.session['done'] = True
    return redirect('client_register_login')
from django.shortcuts import render, redirect

from WorkSphere import settings
from payment.models import Payment
from .models import *
from staticpage.models import *
from freelancer.models import *
import random
import re
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.

def client_register_login(request):
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
        company = request.POST.get('companyname')
        location = request.POST.get('location')
        login = request.POST.get('login')

        if login is not None:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username:
                error_messages = "User Name is Require"

            if not password:
                error_messages = "Password is Required"

            try:
                user = ClientRegisterLogin.objects.get(username=username, password=password)
                request.session['logged_user'] = username
                request.session['role'] = 'CLIENT'
                request.session['show_modal'] = True
                return redirect('client_dashboard')
            except ClientRegisterLogin.DoesNotExist:
                error_messages = 'Invalid username or password.'
                return render(request, 'auth/client_register_login.html', {'error_messages': error_messages})
        
        else:
            # Validation
            if not profile:
                error_message = 'Profile photo is required.'
            elif not firstname:
                error_message = 'First name is required.'
            elif not lastname:
                error_message = 'Last name is required.'
            elif not username:
                error_message = 'Username is required.'
            elif ClientRegisterLogin.objects.filter(username=username).exists():
                error_message = 'Username already exists.'
            else:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not email:
                    error_message = 'Email is required.'
                elif not re.match(email_regex, email):
                    error_message = 'Enter a valid email address.'
                elif ClientRegisterLogin.objects.filter(email=email).exists():
                    error_message = 'Email already exists.'
                elif not password:
                    error_message = 'Password is required.'
                elif len(password) < 8:
                    error_message = 'The password must be at least 8 characters long.'
                elif not any(char.isalpha() for char in password):
                    error_message = 'The password must contain at least one letter.'
                elif not any(char.isdigit() for char in password):
                    error_message = 'The password must contain at least one digit.'
                elif not any(char in "!@#$%^&*(){}[]" for char in password):
                    error_message = 'The password must contain at least one special character.'
                else:
                    phone_regex = r'^\d{10}$'
                    if not phonenumber:
                        error_message = 'Phone number is required.'
                    elif not re.match(phone_regex, phonenumber):
                        error_message = 'Phone number must be exactly 10 digits.'
                    else:
                        register = ClientRegisterLogin(
                            profile_photo=profile,
                            first_name=firstname,
                            last_name=lastname,
                            username=username,
                            email=email,
                            password=password,
                            phone_no=phonenumber,
                            company=company,
                            location=location
                        )

                        try:
                            register.save()
                            # Send confirmation email to client
                            send_mail(
                                subject="Welcome to WorksPhere!",
                                message=f"Dear {firstname},\n\nThank you for registering with WorksPhere as a client. Your account is now active, and you can log in to start posting projects and finding freelancers.\n\nBest regards,\nWorksPhere Team",
                                from_email='worksphere05@gmail.com',
                                recipient_list=[email],
                                fail_silently=False,
                            )

                            # Send notification email to the admin/client management team
                            # admin_email = 'admin@example.com'  # replace with the actual admin email
                            # send_mail(
                            #     subject="New Client Registration on WorksPhere",
                            #     message=f"A new client has registered on WorksPhere:\n\nName: {firstname} {lastname}\nUsername: {username}\nCompany: {company}\nEmail: {email}\nPhone Number: {phonenumber}\nLocation: {location}",
                            #     from_email=settings.DEFAULT_FROM_EMAIL,
                            #     recipient_list=[admin_email],
                            #     fail_silently=False,
                            # )
                            request.session['done'] = True
                            return render(request, 'auth/client_register_login.html', {'success': 'Registration successful.', 'done': request.session['done']})
                        except:
                            request.session['done'] = False
                            error_message = 'Registration failed. Please try again.'

            return render(request, 'auth/client_register_login.html', {'error_message': error_message})

    return render(request, 'auth/client_register_login.html')


def client_forgot_password(request):
    # error_message = None

    if request.method == 'POST':
        user_email = request.POST.get('email')

        # Validation: Check if email is provided
        if not user_email:
            error_message = "Email is required."
        # Validation: Check if email is valid
        elif '@' not in user_email:
            error_message = "Enter a valid email."
        else:
            try:
                user = ClientRegisterLogin.objects.get(email=user_email)

                # Generate OTP and store it in the session
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                request.session['email'] = user.email

                # Send OTP via email
                send_mail(
                    subject='Password Reset',
                    message=f'Your OTP is {otp}',
                    from_email='worksphere05@gmail.com',  # Replace with your sender email
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                # Redirect to OTP verification page
                return redirect('client_verify_otp')

            except ClientRegisterLogin.DoesNotExist:
                error_message = "Email does not exist in our records."

    return render(request, 'auth/client_forgot_password.html', {'error_message': error_message})


def client_verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        # Check if OTP is provided and is a valid 6-digit number
        if not otp:
            error_message = "OTP is required."
        elif not otp.isdigit() or len(otp) != 6:
            error_message = "Please enter a valid 6-digit OTP."
        elif int(otp) != request.session.get('otp'):
            # Check if the entered OTP matches the one stored in the session
            error_message = "Invalid OTP. Please try again."
        else:
            # OTP is correct, redirect to reset password page
            return redirect('client_reset_password')

        # If any validation fails, return to the OTP verification page with an error message
        return render(request, 'auth/client_verify_otp.html', {'error_message': error_message})

    return render(request, 'auth/client_verify_otp.html')


def client_reset_password(request):
    error_message = None  # Initialize error message variable

    if request.method == "POST":
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

        # If everything is valid, reset the password
        else:
            user_email = request.session.get('email')
            user = ClientRegisterLogin.objects.get(email=user_email)
            user.password = password  # Set the new password
            user.save()  # Save the updated user object
            request.session.flush()  # Clear the session
            request.session['done'] = True  # Set a flag indicating successful reset
            return redirect('client_register_login')  # Redirect to login page

    return render(request, 'auth/client_reset_password.html')


def client_contact(request):
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
            return render(request, 'client_contact.html', {'error_message': errors_message})
        

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
            return render(request, 'client_dashboard.html')
        except:
            return render(request, 'client_contact.html', {'error': 'Failed to save contact information.'})
    return render(request, 'client_contact.html') 

def client_post_project(request):
    username = request.session.get('logged_user')
    client = ClientRegisterLogin.objects.get(username=username)

    error_message = None  # Initialize error_message as None
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('categories')
        budget = request.POST.get('budget')
        budget_type = request.POST.get('budget_type')
        skills = request.POST.get('skills')
        experience_level = request.POST.get('experience_level')
        deadline = request.POST.get('deadline')
        image = request.FILES.get('image')
        attachments = request.FILES.get('attachments')  # Use getlist to handle multiple attachments

        # Validation

        if not image:
            error_message = 'Project photo is require'
            
        if not title:
            error_message = 'Title is required.'
        
        elif not description:
            error_message = 'Description is required.'
        
        elif not category:
            error_message = 'Category is required.'
        
        elif not budget:
            error_message = 'Budget is required.'
        
        elif not budget_type:
            error_message = 'Budget type is required.'
        
        elif not skills:
            error_message = 'Skills are required.'
        
        elif not experience_level:
            error_message = 'Experience level is required.'
        
        elif not deadline:
            error_message = 'Deadline is required.'

        if error_message:
            return render(request, 'client_post_project.html', {'error_message': error_message })

        # Create project
        project = ClientPostProject(
            client=client,
            title=title,
            description=description,
            category=category,
            budget=budget,
            budget_type=budget_type,
            skills_required=skills,
            experience_level=experience_level,
            deadline=deadline,
            photo=image,
            status = 'open'
        )

        try:
            project.save()

            # Save attachments if present
            for attachment in attachments:
                project.attachments.create(file=attachment)

            return redirect('client_list_of_project')
        except:
            return render(request, 'client_post_project.html', {'error_message': 'Failed to save project information.'})

    return render(request, 'client_post_project.html')

def client_freelancer_profile(request):
    return render(request, 'client_freelancer_profile.html')

def client_job_details(request, project_id):
    username = request.session.get('logged_user')
    client = ClientRegisterLogin.objects.get(username = username)
    details = ClientPostProject.objects.get(id=project_id, client=client)
    skills = details.skills_required.split(',')  # Assuming skills are stored as a comma-separated string
    
    context = {
        'details' : details,
        'skills' : skills,
    }
    return render(request, 'client_job_details.html', context)

def client_list_of_project(request):
    username = request.session.get('logged_user')
    client = ClientRegisterLogin.objects.get(username = username)
    projects = ClientPostProject.objects.filter(client=client)

    context={
        'projects' : projects,
        'details': {'description': 'Your project description <br> with <strong>HTML</strong> formatting here.'}, # Replace with actual project details
    }
    return render(request, 'client_list_of_project.html', context)

def client_profile(request):
    username = request.session.get('logged_user')
    client = ClientRegisterLogin.objects.get(username=username)

    context ={
        'client' : client,
    }
    return render(request, 'client_profile.html', context)

def client_edit_profile(request):
    username = request.session.get('logged_user')
    client = ClientRegisterLogin.objects.get(username=username)

    if request.method == "POST":
        bio = request.POST.get('bio')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        company = request.POST.get('company')

        if bio:
            client.bio = bio
        if password:
            client.password = password
        if phone:
            client.phone_no = phone
        if location:
            client.location = location
        if company:
            client.company = company

        client.save()

        return redirect('client_profile')

    context = {
        'client': client,
    }

    return render(request, 'client_edit_profile.html', context)

def client_received_proposal(request):
    user = request.session.get('logged_user')
    client = ClientRegisterLogin.objects.get(username=user)  # Get the logged-in client
    # Get all projects for this client
    client_projects = ClientPostProject.objects.filter(client=client)
    # Fetch the proposals related to this client's projects
    proposals = FreelancerProposal.objects.filter(project__in=client_projects)
    # Now filter all proposals for that project ID
    selected_proposals = proposals.filter(project__in=client_projects)
    # Prepare context data to pass to the template
    context = {
        'client': client,
        'proposals': proposals,  
        'selected_proposal': selected_proposals,
    }

    return render(request, 'client_received_proposal.html', context)

def client_payment(request):
    # Fetch all payments with status 'Completed' from the database
    payments = Payment.objects.filter(status="Completed")

    # Pass the filtered payments to the template
    return render(request, 'client_payment.html', {'payments': payments})

def client_dashboard(request):
    return render(request, 'client_dashboard.html')

def header_1(request):
    return render(request, 'header_1.html')

def header_2(request):
    return render(request, 'header_2.html')

def header_3(request):
    return render(request, 'header_3.html')

def client_logout(request):
    request.session.flush()
    request.session['done'] = True
    return redirect('client_register_login')
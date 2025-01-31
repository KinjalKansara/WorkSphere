import datetime
from pyexpat.errors import messages
from django.shortcuts import render, redirect

from WorkSphere import settings
from administrator.models import AdminUser
from notification.models import Notification
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
                                subject="Welcome to WorkSphere!",
                                message=f"Dear {firstname},\n\nThank you for registering with WorkSphere as a client. Your account is now active, and you can log in to start posting projects and finding freelancers.\n\nBest regards,\nWorkSphere Team",
                                from_email='worksphere05@gmail.com',
                                recipient_list=[email],
                                fail_silently=False,
                            )

                            # Send notification email to the admin/client management team
                            admin_email = 'worksphere05@gmail.com'  # replace with the actual admin email
                            send_mail(
                                subject="New Client Registration on WorkSphere",
                                message=f"A new client has registered on WorkSphere:\n\nName: {firstname} {lastname}\nUsername: {username}\nCompany: {company}\nEmail: {email}\nPhone Number: {phonenumber}\nLocation: {location}",
                                from_email='worksphere05@gmail.com',
                                recipient_list=[admin_email],
                                fail_silently=False,
                            )

                             # Corrected notification creation
                            notification = Notification(
                                title="New client registered",
                                message=f"{firstname} {lastname} has registered as a client.",
                                notification_type='admin',
                                username=username,  # Provide the username of the new client
                            )

                            # Create a notification for the registered client
                            Notification.objects.create(
                                title="Welcome to WorkSphere!",
                                message=f"Dear {firstname},\n\nThank you for registering with WorkSphere as a client. You can now start posting projects and finding freelancers who match your needs. We look forward to seeing you create and collaborate!\n\nBest regards,\nWorkSphere Team",
                                notification_type='client',
                                username=username,
                                is_read=False
                            )

                            # Save the notification to the database
                            notification.save()

                            request.session['done'] = True
                            return render(request, 'auth/client_register_login.html', {'success': 'Registration successful.', 'done': request.session['done']})
                        except Exception as e:
                            print(e)  # Log the error for debugging
                            request.session['done'] = False
                            error_message = 'Registration failed. Please try again.'

            return render(request, 'auth/client_register_login.html', {'error_message': error_message})

    return render(request, 'auth/client_register_login.html')



def client_forgot_password(request):
    error_message = None

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
                request.sesstion['check_email'] = user.email

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
    if request.session.get('check_email') is None:
        return redirect('client_register_login')

    error_message = None
    
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
    if request.session.get('check_email') is None:
        return redirect('client_register_login')

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
    try:
        # Attempt to get the logged-in user from the session
        username = request.session.get('logged_user')
        if not username:
            raise ValueError("Session expired or user not logged in.")

        client = ClientRegisterLogin.objects.get(username=username)

    except (ClientRegisterLogin.DoesNotExist, ValueError) as e:
        return redirect('client_register_login')  # Redirect to login page if session is invalid or user is not found

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
            error_message = 'Project photo is required'
        elif not title:
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
            attachments=attachments,
            status='open'
        )

        try:
            project.save()
            # Send email notification to the client who posted the project
            subject = f"New Project Posted: {title}"
            message = f"Hello {client.first_name} {client.last_name},\n\nYour project titled '{title}' has been successfully posted on WorksPhare.\n\nDetails:\nDescription: {description}\n\nCategory: {category}\n\nBudget: {budget}\n\nDeadline: {deadline}\n\nBest regards,\nWorkPshere Team"
            from_email = 'worksphere05@gmail.com'
            recipient_list = [client.email]
            send_mail(subject, message, from_email, recipient_list)

            # Send email to all registered freelancers
            freelancers = FreelancerRegisterLogin.objects.all()
            freelancer_emails = [freelancer.email for freelancer in freelancers]

            # Email to freelancers
            for freelancer in freelancers:
                subject_for_freelancers = f"New Project Posted: {title} - Check it out!"
                message_for_freelancers = f"Hello {freelancer.first_name} {freelancer.last_name},\n\nA new project titled '{title}' has been posted by {client.first_name} {client.last_name}. You may be interested in submitting a proposal.\n\nDetails:\nDescription: {description}\nCategory: {category}\nBudget: {budget}\nDeadline: {deadline}\n\nBest regards,\nWorkSphere Team"
                
                # Send email only to freelancers whose email exists
                send_mail(subject_for_freelancers, message_for_freelancers, from_email, [freelancer.email])

            # Create notifications for the client, freelancer, and admin
            Notification.objects.create(
                title="Your Project is Posted Successfully",
                message=f"Your project titled '{title}' has been successfully posted on WorkSphere!",
                notification_type='client',
                username=client.username,
                is_read=False
            )

            # Get freelancers who match the skills (assuming skills match logic should be implemented here)
            freelancers_with_matching_skills = FreelancerRegisterLogin.objects.filter(skills__contains=skills)

            for freelancer in freelancers_with_matching_skills:
                # Create a notification for each freelancer who matches the skills
                Notification.objects.create(
                    title="New Project Posted",
                    message=f"New project titled '{title}' posted by {client.first_name} {client.last_name}. You may be interested in submitting a proposal.",
                    notification_type='freelancer',
                    username=freelancer.username,
                    is_read=False
                )

            # Notification for admin
            Notification.objects.create(
                title="New Project Posted by Client",
                message=f"A new project titled '{title}' has been posted by {client.first_name} {client.last_name}. Please review the project details.",
                notification_type='admin',
                username='ADMIN',  # Assuming you have an 'ADMIN' user
                is_read=False
            )

            return redirect('client_list_of_project')
        except Exception as e:
            return render(request, 'client_post_project.html', {'error_message': f'Failed to save project information: {str(e)}'})

    return render(request, 'client_post_project.html')


def client_job_details(request, project_id):
    try:
        # Attempt to get the logged-in user from the session
        username = request.session.get('logged_user')
        if not username:
            raise ValueError("Session expired or user not logged in.")

        client = ClientRegisterLogin.objects.get(username=username)
        details = ClientPostProject.objects.get(id=project_id, client=client)
        skills = details.skills_required.split(',')  # Assuming skills are stored as a comma-separated string
        
        context = {
            'details': details,
            'skills': skills,
        }
        return render(request, 'client_job_details.html', context)

    except (ClientRegisterLogin.DoesNotExist, ClientPostProject.DoesNotExist, ValueError):
        return redirect('client_register_login')  # Redirect to login if user or project is not found


def client_list_of_project(request):
    try:
        # Attempt to get the logged-in user from the session
        username = request.session.get('logged_user')
        if not username:
            raise ValueError("Session expired or user not logged in.")

        client = ClientRegisterLogin.objects.get(username=username)

        # Fetch projects associated with the client and order by date (descending)
        projects = ClientPostProject.objects.filter(client=client).order_by('-created_at')

        context = {
            'projects': projects,
            'details': {'description': 'Your project description <br> with <strong>HTML</strong> formatting here.'},
        }
        return render(request, 'client_list_of_project.html', context)

    except (ClientRegisterLogin.DoesNotExist, ValueError):
        return redirect('client_register_login')  # Redirect to login if session is invalid or user not found


def client_profile(request):
    try:
        # Attempt to get the logged-in user from the session
        username = request.session.get('logged_user')
        if not username:
            raise ValueError("Session expired or user not logged in.")

        client = ClientRegisterLogin.objects.get(username=username)

        context = {
            'client': client,
        }
        return render(request, 'client_profile.html', context)

    except (ClientRegisterLogin.DoesNotExist, ValueError):
        return redirect('client_register_login')  # Redirect to login if session is invalid or user not found


def client_edit_profile(request):
    try:
        # Attempt to get the logged-in user from the session
        username = request.session.get('logged_user')
        if not username:
            raise ValueError("Session expired or user not logged in.")

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
                client.password = password  # Consider hashing the password before saving
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

    except (ClientRegisterLogin.DoesNotExist, ValueError):
        return redirect('client_register_login')  # Redirect to login if session is invalid or user not found


def client_received_proposal(request):
    try:
        # Attempt to get the logged-in user from the session
        user = request.session.get('logged_user')
        if not user:
            raise ValueError("Session expired or user not logged in.")

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

    except (ClientRegisterLogin.DoesNotExist, ValueError):
        return redirect('client_register_login')  # Redirect to login if session is invalid or user not found


def client_payment(request):
    try:
        # Attempt to get the logged-in user from the session
        username = request.session.get('logged_user')
        if not username:
            raise ValueError("Session expired or user not logged in.")

        client = ClientRegisterLogin.objects.get(username=username)  # Ensure the client exists

        # Fetch all payments with status 'Completed' from the database
        payments = Payment.objects.filter(status="Completed")

        # Pass the filtered payments to the template
        return render(request, 'client_payment.html', {'payments': payments})

    except (ClientRegisterLogin.DoesNotExist, ValueError):
        return redirect('client_register_login')  # Redirect to login if session is invalid or user not found


def client_dashboard(request):
    return render(request, 'client_dashboard.html')



def client_submitted_project(request):
    try:
        # Attempt to get the logged-in user from the session
        user = request.session.get('logged_user')
        if not user:
            raise ValueError("Session expired or user not logged in.")

        client = ClientRegisterLogin.objects.get(username=user)

        # Get the client's received proposals (proposals from freelancers)
        received_proposals = FreelancerProposal.objects.filter(client=client, status='Completed')
        freelancer = FreelancerRegisterLogin.objects.all()

        context = {
            'completed_projects': received_proposals,
            'freelancer': freelancer
        }
        return render(request, 'client_submitted_project.html', context)

    except (ClientRegisterLogin.DoesNotExist, ValueError):
        return redirect('client_register_login')  # Redirect to login if session is invalid or user not found


def client_notification(request):
    try:
        # Attempt to get the logged-in user from the session
        username = request.session.get('logged_user')
        role = request.session.get('role')  # e.g., 'ADMIN', 'CLIENT', 'FREELANCER'

        if not username or not role:
            raise ValueError("Session expired or invalid role.")

        # Query notifications based on role
        if role == 'ADMIN':
            # Admin gets all notifications of type 'admin'
            notifications = Notification.objects.filter(notification_type='admin').order_by('-created_at')
        elif role == 'CLIENT':
            # Clients see notifications sent to 'ALL_CLIENTS' or their specific username
            notifications = Notification.objects.filter(notification_type='client').order_by('-created_at')
        elif role == 'FREELANCER':
            # Freelancers see notifications sent to their specific username
            notifications = Notification.objects.filter(notification_type='freelancer').order_by('-created_at')
        else:
            # Invalid role, redirect to login or handle accordingly
            return redirect('client_register_login')

        context = {
            'notifications': notifications,
        }
        return render(request, 'client_notification.html', context)

    except ValueError:
        return redirect('client_register_login')  # Redirect to login if session is invalid or role is missing


def client_services(request):
    return render(request, 'client_services.html')

def header_1(request):
    return render(request, 'header_1.html')

def header_2(request):
    # if request.session.get('role') != 'CLIENT':
    #     return redirect('client_register_login')  # Redirect to login if not a client
    return render(request, 'header_2.html')

def header_3(request):
    return render(request, 'header_3.html')

def client_logout(request):
    request.session.flush()
    request.session['done'] = True
    return redirect('client_register_login')
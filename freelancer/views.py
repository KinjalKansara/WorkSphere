import datetime
from decimal import Decimal
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from WorkSphere import settings
from administrator.models import AdminUser
from notification.models import Notification
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

                # Create a notification for the admin
                Notification.objects.create(
                    title="New Freelancer Registered",
                    message=f"{firstname} {lastname} has registered as a freelancer.",
                    notification_type='admin',
                    username=username,
                    is_read=False
                )

                # Create a notification for the client
                Notification.objects.create(
                    title="New Freelancer Registered",
                    message=f"{firstname} {lastname} has registered as a freelancer.",
                    notification_type='client',
                    username=username,
                    is_read=False
                )

                # Create a notification for the registered freelancer
                Notification.objects.create(
                    title="Welcome to WorksPhere!",
                    message="Thank you for registering as a freelancer. Start exploring projects and showcasing your skills!",
                    notification_type='freelancer',
                    username=username,
                    is_read=False
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

import random

def freelancer_list_of_project(request):
    # Fetch all open projects
    projects = list(ClientPostProject.objects.filter(status='open'))  # Convert queryset to a list
    
    # Shuffle the list of projects
    random.shuffle(projects)
    
    context = {
        'projects': projects,
        # Additional context if needed
        'details': {
            'description': 'Your project description <br> with <strong>HTML</strong> formatting here.'
        },
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
        bank_name = request.POST.get('bank_name')
        bank_ifsc = request.POST.get('ifsc_code')
        account_number = request.POST.get('account_number')

        errors_message = None

        # Validate bank details
        if bank_name and len(bank_name.strip()) == 0:
            errors_message = "Bank name cannot be empty."
        
        if bank_ifsc and (len(bank_ifsc.strip()) != 11 or not bank_ifsc.isalnum()):
            errors_message = "IFSC Code must be 11 alphanumeric characters."

        if account_number and not account_number.isdigit():
            errors_message = "Account number must contain only digits."

        # If there is an error, return the template with the error message and existing data
        if errors_message:
            context = {
                'freelancer': freelancer,
                'error_message': errors_message,
            }
            return render(request, 'freelancer_edit_profile.html', context)

        # Update freelancer details
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
        if bank_name:
            freelancer.bank_name = bank_name
        if bank_ifsc:
            freelancer.ifsc_code = bank_ifsc
        if account_number:
            freelancer.account_number = account_number

        # Save the updated data
        freelancer.save()

        return redirect('freelancer_profile')

    # Render the initial page with the freelancer's data
    context = {
        'freelancer': freelancer,
    }
    return render(request, 'freelancer_edit_profile.html', context)



def confirm_proposal(request):
    user = request.session.get('logged_user')  # Get the logged-in user's session
    freelancer = FreelancerRegisterLogin.objects.get(username=user)
    
    # Fetching proposals related to the freelancer
    proposals = Payment.objects.filter(proposal__freelancer=freelancer)

    if request.method == 'POST':
        proposal_id = request.POST.get('proposal_id')

        try:
            proposal = FreelancerProposal.objects.get(id=proposal_id)
            proposal.status = 'Completed'  # Change proposal status to 'Completed'

            # Save the proposal status change
            proposal.save()

            # Send email to freelancer notifying them about the proposal completion
            subject = f"Proposal for '{proposal.project.title}' has been Confirmed"
            message = f"Hello {freelancer.first_name},\n\nCongratulations! Your proposal for the project '{proposal.project.title}' has been confirmed and completed by the client.\n\nDetails:\nTitle: {proposal.project.title}\nBid: ${proposal.bid}\n\nBest regards,\nWorksPhere Team"
            from_email = 'worksphere05@gmail.com'
            recipient_list = [freelancer.email]
            send_mail(subject, message, from_email, recipient_list)

            # Send a notification to the freelancer about the proposal confirmation
            Notification.objects.create(
                title="Proposal Confirmed",
                message=f"Your proposal for the project '{proposal.project.title}' has been confirmed and marked as completed.",
                notification_type='freelancer',
                username=freelancer.username,
                is_read=False
            )

            # Send a notification to the client about the proposal completion
            client = proposal.client  # Fetch the client related to the proposal's project
            Notification.objects.create(
                title="Proposal Completed",
                message=f"Your proposal for the project '{proposal.project.title}' has been completed by {freelancer.first_name} {freelancer.last_name}.",
                notification_type='client',
                username=client.username,  # Use the client's username
                is_read=False
            )

            # Send a notification to the admin about the proposal confirmation
            Notification.objects.create(
                title="Proposal Completed",
                message=f"Freelancer {freelancer.first_name} {freelancer.last_name} has completed the proposal for the project '{proposal.project.title}' posted by {client.first_name} {client.last_name}.",
                notification_type='admin',
                username='ADMIN',
                is_read=False
            )

            return redirect('freelancer_submitted_project')

        except FreelancerProposal.DoesNotExist:
            error_message = 'Freelancer proposal does not exist.'
        except Payment.DoesNotExist:
            error_message = 'Payment is not done.'

    context = {
        'proposals': proposals  # Change variable name for clarity
    }

    return render(request, 'confirm_proposal.html', context)


# def confirm_proposal(request):
#     user = request.session.get('logged_user')
#     try:
#         freelancer = FreelancerRegisterLogin.objects.get(username=user)
#     except FreelancerRegisterLogin.DoesNotExist:
#         messages.error(request, 'Freelancer not found!')
#         return redirect('error_page')

#     # Fetching proposals related to the freelancer (including payment status)
#     proposals = ProjectPayments.objects.filter(proposal__freelancer=freelancer)

#     if request.method == 'POST':
#         proposal_id = request.POST.get('proposal_id')

#         try:
#             proposal = FreelancerProposal.objects.get(id=proposal_id)
#             payment = ProjectPayments.objects.get(proposal=proposal)

#             # Remove proposal from Payment (effectively confirming it)
#             payment.delete()

#             messages.success(request, 'Your proposal has been successfully confirmed!')
#             return redirect('freelancer_submitted_project')

#         except FreelancerProposal.DoesNotExist:
#             messages.error(request, 'Proposal not found!')
#             return redirect('error_page')
#         except ProjectPayments.DoesNotExist:
#             messages.error(request, 'Payment details not found!')
#             return redirect('error_page')

#     context = {
#         'proposals': proposals
#     }
#     return render(request, 'confirm_proposal.html', context)


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
    try:
        freelancer = FreelancerRegisterLogin.objects.get(username=user)  # Get the freelancer object
        project = ClientPostProject.objects.get(id=project_id)
        client = project.client

        context = {
            'project': project,
            'freelancer': freelancer,
            'client': client,
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
                you_receive = 0.00  # Amount freelancer will receive
            
            cover_letter = request.POST.get('cover_letter')
            attachment = request.FILES.get('attachment')

            # Create a FreelancerProposal object and associate it with the logged-in freelancer
            proposal = FreelancerProposal(
                freelancer=freelancer,
                project=project,
                client=client,
                title=title,
                description=description,
                duration=duration,
                bid=bid,
                cover_letter=cover_letter,
                attachment=attachment,
            )
            try:
                proposal.save()

                # Email to freelancer confirming proposal submission
                subject = f"Proposal Submitted for '{title}'"
                message = f"Hello {freelancer.first_name},\n\nYou have successfully submitted your proposal for the project titled '{title}'.\n\nDetails:\nDescription: {description}\nBid: ${bid}\nDuration: {duration} days\n\nYou will be notified if the client accepts your proposal.\n\nBest regards,\nWorksPhere Team"
                from_email = 'worksphere05@gmail.com'
                recipient_list = [freelancer.email]
                send_mail(subject, message, from_email, recipient_list)

                # Email to client notifying them of the new proposal
                subject_for_client = f"New Proposal Submitted for '{title}'"
                message_for_client = f"Hello {client.first_name},\n\nA freelancer has submitted a proposal for your project titled '{title}'.\n\nDetails:\nFreelancer: {freelancer.first_name} {freelancer.last_name}\nBid: ${bid}\nDuration: {duration} days\n\nYou can review the proposal and decide whether to accept it.\n\nBest regards,\nWorksPhere Team"
                send_mail(subject_for_client, message_for_client, from_email, [client.email])

                # Create notifications for freelancer and client
                Notification.objects.create(
                    title="Proposal Submitted",
                    message=f"You have successfully submitted your proposal for the project '{title}'.",
                    notification_type='freelancer',
                    username=freelancer.username,
                    is_read=False
                )

                Notification.objects.create(
                    title="New Proposal for Your Project",
                    message=f"A freelancer has submitted a proposal for your project titled '{title}'. Please review it.",
                    notification_type='client',
                    username=client.username,
                    is_read=False
                )

                return redirect('freelancer_proposal')  # Redirect to the freelancer's proposal list page
            except Exception as e:
                print(e)
                context['error_message'] = 'Error submitting proposal. Please try again.'
    except (FreelancerRegisterLogin.DoesNotExist, ClientPostProject.DoesNotExist):
        return render(request, '404.html', {'error_message': 'Project or freelancer not found.'})

    return render(request, 'freelancer_send_proposal.html', context)



# Freelancer's completed proposals (those marked as completed)
def freelancer_submitted_project(request):
    user = request.session.get('logged_user')
    try:
        freelancer = FreelancerRegisterLogin.objects.get(username=user)
    except FreelancerRegisterLogin.DoesNotExist:
        messages.error(request, 'Freelancer not found!')
        return redirect('error_page')
    
    # Get the freelancer's completed proposals (those marked as completed)
    submitted_proposals = FreelancerProposal.objects.filter(freelancer=freelancer, status='Completed')
    context = {
        'completed_proposals': submitted_proposals
    }

    return render(request, 'freelancer_submitted_project.html', context)


def freelancer_notification(request):
    # Determine the role of the logged-in user
    username = request.session.get('logged_user')
    role = request.session.get('role')  # e.g., 'ADMIN', 'CLIENT', 'FREELANCER'


    # Query notifications based on role
    if role == 'ADMIN':
        # Admin gets all notifications of type 'admin'
        notifications = Notification.objects.filter(notification_type='admin').order_by('-created_at')
    elif role == 'CLIENT':
        # Clients see notifications sent to 'ALL_CLIENTS' or their specific username
        notifications = Notification.objects.filter(notification_type='client',).order_by('-created_at')
    elif role == 'FREELANCER':
        # Freelancers see notifications sent to their specific username
        notifications = Notification.objects.filter(notification_type='freelancer').order_by('-created_at')
    else:
        # Invalid role, redirect to login or handle accordingly
        return redirect('login')

    context = {
        'notifications': notifications,
    }
    
    return render(request, 'freelancer_notification.html',context)

# def complete_project(request):
#     if request.method == "POST":
#         proposal_id = request.POST.get('proposal_id')
        
#         # Retrieve the proposal
#         proposal = get_object_or_404(FreelancerProposal, id=proposal_id)
        
#         # Mark project and proposal as completed
#         try:
#             # Update the proposal status (add a `status` field in FreelancerProposal if necessary)
#             proposal.status = 'completed'  # Add this field in your model if it doesn't exist
#             proposal.save()

#             # Mark the project as completed (add a `status` field in ClientPostProject if necessary)
#             project = proposal.project
#             project.status = 'completed'  # Add this field in your model if it doesn't exist
#             project.save()

#             # Redirect based on user type
#             if request.user.is_freelancer:  # Assume a `is_freelancer` field exists on the user model
#                 return redirect('freelancer_completed_projects')  # Freelancer's completed projects page
#             elif request.user.is_client:  # Assume a `is_client` field exists on the user model
#                 return redirect('client_completed_projects')  # Client's completed projects page

#         except Exception as e:
#             print(f"Error: {e}")
#             return HttpResponse("Something went wrong.", status=500)

#     return HttpResponse("Invalid request method.", status=405)

def freelancer_services(request):
    return render(request, 'freelancer_services.html')

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
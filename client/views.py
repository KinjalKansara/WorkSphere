from django.shortcuts import render, redirect
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

            try:
                user = ClientRegisterLogin.objects.get(username=username, password=password)
                request.session['logged_user'] = username
                request.session['role'] = 'CLIENT'
                request.session['show_modal'] = True
                return redirect('client_dashboard')
            except ClientRegisterLogin.DoesNotExist:
                error_message = 'Invalid username or password.'
                return render(request, 'auth/client_register_login.html', {'error_message': error_message})
        
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
                            request.session['done'] = True
                            return render(request, 'auth/client_register_login.html', {'success': 'Registration successful.', 'done': request.session['done']})
                        except:
                            request.session['done'] = False
                            error_message = 'Registration failed. Please try again.'

            return render(request, 'auth/client_register_login.html', {'error_message': error_message})

    return render(request, 'auth/client_register_login.html')


def client_forgot_password(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user = ClientRegisterLogin.objects.get(email=user_email)

        if user:
            otp = random.randint(100000,999999)
            request.session['otp']= otp
            request.session['email']= user.email

            send_mail(
                subject='Password Reset',
                message=f'Your OTP is {otp}',
                from_email='worksphere05@gmail.com',  # Replace with your sender email
                recipient_list=[user.email],
                fail_silently=False,
            )
            return redirect('client_verify_otp')
    return render(request, 'auth/client_forgot_password.html')

def client_verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if request.session.get('otp') == int(otp):
            return redirect('client_reset_password')
        else:
            return redirect('client_verify_otp')
    return render(request, 'auth/client_verify_otp.html')

def client_reset_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user_email = request.session.get('email')
            user = ClientRegisterLogin.objects.get(email=user_email)
            user.password = password
            user.save()
            request.session.flush()
            request.session['done'] = True
            return redirect('client_register_login')
        else:
            return redirect('client_reset_password')

    return render(request, 'auth/client_reset_password.html')

@login_required(login_url='client_register_login')
def client_contact(request):
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
            return render(request, 'client_dashboard.html')
        except:
            return render(request, 'client_contact.html', {'error': 'Failed to save contact information.'})
    return render(request, 'client_contact.html') 

def client_post_project(request):
    username = request.session.get('logged_user')
    client = ClientRegisterLogin.objects.get(username = username)

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
        attachments = request.FILES.get('attachments')

        # Validation
        errors = {}

        if not title:
            errors['title'] = 'Title is required.'
        
        if not description:
            errors['description'] = 'Description is required.'
        
        if not category:
            errors['category'] = 'Category is required.'
        
        if not budget:
            errors['budget'] = 'Budget is required.'
        
        if not budget_type:
            errors['budget_type'] = 'Budget type is required.'
        
        if not skills:
            errors['skills'] = 'Skills are required.'
        
        if not experience_level:
            errors['experience_level'] = 'Experience level is required.'
        
        if not deadline:
            errors['deadline'] = 'Deadline is required.'

        if errors:
            return render(request, 'client_post_project.html', {'errors': errors})

        project = ClientPostProject(
            client = client,
            title=title,
            description=description,
            category=category,
            budget=budget,
            budget_type=budget_type,
            skills_required=skills,
            experience_level=experience_level,
            deadline=deadline,
            photo=image,
            attachments = attachments
        )

        try:
            project.save()
            # for attachment in attachments:
            #     project.attachments.create(file=attachment)
            return redirect('client_list_of_project')
        except:
            return render(request, 'client_post_project.html', {'error': 'Failed to save project information.'})

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

    # Prepare context data to pass to the template
    context = {
        'client': client,
        'proposals': proposals,
    }

    return render(request, 'client_received_proposal.html', context)



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
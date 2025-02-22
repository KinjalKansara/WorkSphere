from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from notification.models import Notification
from payment.models import Payment
from .models import *
from staticpage.models import *
from client.models import *
from freelancer.models import *
from django.template.loader import get_template
from xhtml2pdf import pisa
import random
import re
from django.core.mail import send_mail

# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        error_message = None

        if not email:
            error_message = "Admin Name is Required"
        
        if not password:
            error_message = "Password is Required"

        if error_message:
            return render(request, 'auth/admin_login.html', {'error_message': error_message})

        try:
            user = AdminUser.objects.get(email=email, password=password)
            request.session['admin'] = email
            request.session['role'] = 'ADMIN'
            return redirect('admin_dashboard')

        except AdminUser.DoesNotExist:
            error_message = 'Invalid username or password.'
            return render(request, 'auth/admin_login.html', {'error_message': error_message})
    
    return render(request, 'auth/admin_login.html')


def admin_forgot_password(request):
    error_message = None
    
    if request.method == 'POST':
        user_email = request.POST.get('email')

        if not user_email:
            error_message = "Email is required."
        # Validation: Check if email exists in the database
        elif '@' not in user_email:
            error_message = "Enter a valid email."
        else:
            try:
                user = AdminUser.objects.get(email=user_email)
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                request.session['email'] = user.email
                request.session['check_email'] = user.email

                # Send OTP via email
                send_mail(
                    subject='Password Reset',
                    message=f'Your OTP is {otp}',
                    from_email='worksphere05@gmail.com',  # Replace with your sender email
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                return redirect('admin_verify_otp')
            except AdminUser.DoesNotExist:
                error_message = "Email not found in our records."

    return render(request, 'auth/admin_forgot_password.html', {'error_message': error_message})

def admin_verify_otp(request):
    if request.session.get('check_email') is None:
        return redirect('admin_login')
    
    error_message = None
    
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
            return redirect('admin_reset_password')
        
        return render(request, 'auth/admin_verify_otp.html', {'error_message': error_message})
    
    return render(request, 'auth/admin_verify_otp.html')

def admin_reset_password(request):
    if request.session.get('check_email') is None:
        return redirect('admin_login')
    
    error_message = None

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

        if error_message:
            return render(request, 'auth/admin_reset_password.html', {'error_message': error_message})

        else:
            user_email = request.session.get('check_email')
            user = AdminUser.objects.get(email=user_email)
            user.password = password
            user.save()
            return redirect('admin_login')
    return render(request, 'auth/admin_reset_password.html')

def admin_dashboard(request):   
    return render(request, 'admin_dashboard.html')

def admin_profile(request):
    if not request.session.get('admin'):
        return redirect('admin_login')
    
    admin = AdminUser.objects.first()

    context={
        'admin':admin,
    }
    return render(request, 'admin_profile.html',context)

def admin_edit_profile(request):
    try:
        if not request.session.get('admin'): 
            return redirect('admin_login') 

        admin = AdminUser.objects.first()

        if request.method == 'POST':
            password = request.POST.get('password')

            if password:
                admin.password = password

            admin.save()

            return redirect('admin_profile')

        context = {
            'admin' : admin,
        }

        return render(request, 'admin_edit_profile.html', context)
    except(AdminUser.DoesNotExist, ValueError):
        return redirect('client_edit_profile')



def admin_contact(request):
    if not request.session.get('admin'): 
        return redirect('admin_login') 
    
    contact = ClientContact.objects.all()
    admin_email = request.session.get('admin') 

    context = { 
        'contact': contact, 
        'admin_email': admin_email, 
        }

    return render(request, 'admin_contact.html', context)

def send_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user_message = request.POST.get('message')
        
        # Construct the proper email message
        message = f"""
        Dear User,

        Thank you for reaching out to us.

        We have reviewed your query, and here is our response:

        {user_message}

        We hope this addresses your concern. If you have any further questions or need additional assistance, please don’t hesitate to contact us directly. We are always here to help.

        Thank you for your patience and understanding.

        Best regards,  
        Your Team
        """

        send_mail(
            'Reply to Your Query',
            message,
            'worksphere05@gmail.com',  # Replace with your admin email
            [email],
            fail_silently=False,
        )
        return redirect('admin_contact')  # Replace with your contact page URL


def admin_delete_contact(request, id):
    # Get the contact by ID
    try:
        contact = ClientContact.objects.get(id=id)
    except ClientContact.DoesNotExist:
        return redirect('admin_contact')  # If the contact doesn't exist, redirect back

    # Send email notification before deleting
    subject = "Your Contact Information Has Been Deleted"
    message = f"Dear {contact.first},\n\nYour contact information has been deleted from our system.\n\nBest regards,\nWorkSphere"
    from_email = 'worksphere05@gmail.com'
    recipient_list = [contact.email]

    # Send the email
    send_mail(subject, message, from_email, recipient_list)

    # Delete the contact
    contact.delete()

    # Redirect back to the contact list page
    return redirect('admin_contact')


def admin_client(request):
    if not request.session.get('admin'):
        return render('admin_login')
    
    client = ClientRegisterLogin.objects.all()
    admin_email = request.session.get('admin')

    context ={
        'clients' : client,
        'admin_email' : admin_email,
    }
    return render(request, 'admin_client.html', context)

def admin_delete_client(request, id):
    try:
        # Get the client by ID
        client = ClientRegisterLogin.objects.get(id=id)
    except ClientRegisterLogin.DoesNotExist:
        # If the client doesn't exist, redirect back to the client list page
        return redirect('admin_client')

    # Send email notification before deleting
    subject = "Your Account Has Been Deleted"
    message = f"Dear {client.first_name},\n\nWe regret to inform you that your account has been deleted from our system. If you have any questions, please contact support.\n\nBest regards,\nWorkSphere"
    from_email = 'worksphere05@gmail.com'  # Replace with your email address
    recipient_list = [client.email]

    # Send the email to the client
    send_mail(subject, message, from_email, recipient_list)

    # Delete the client
    client.delete()

    # Redirect back to the client list page
    return redirect('admin_client')

def admin_freelancer(request):
    # Check if the admin session exists; if not, redirect to login
    if not request.session.get('admin'): 
        return redirect('admin_login') 
    
    # Fetch all freelancers
    freelancer = FreelancerRegisterLogin.objects.all()
    
    # Get admin's email from the session
    admin_email = request.session.get('admin') 

    # Pass the freelancer data and admin email to the template context
    context = {
        'freelancer': freelancer,
        'admin_email': admin_email,
    }

    # Render the template with the context data
    return render(request, 'admin_freelancer.html', context)


def freelancer_delete_details(request, id):
    try:
        # Get the freelancer by ID
        freelancer = FreelancerRegisterLogin.objects.get(id=id)
    except FreelancerRegisterLogin.DoesNotExist:
        # If the freelancer doesn't exist, redirect back to the freelancer list page
        return redirect('admin_freelancer')

    # Send email notification before deleting
    subject = "Your Freelancer Account Has Been Deleted"
    message = f"Dear {freelancer.first_name},\n\nWe regret to inform you that your freelancer account has been deleted from our system. If you have any questions, please contact support.\n\nBest regards,\nWorkSphere"
    from_email = 'worksphere05@gmail.com'  # Replace with your email address
    recipient_list = [freelancer.email]

    # Send the email to the freelancer
    send_mail(subject, message, from_email, recipient_list)

    # Delete the freelancer details
    freelancer.delete()

    # Redirect back to the freelancer list page
    return redirect('admin_freelancer')


def admin_payment(request):
    # Fetch all payments
    payments = Payment.objects.select_related(
        'proposal__client', 
        'proposal__freelancer', 
        'proposal__project'
    )
    
    context = {
        'payment': payments
    }
    return render(request, 'admin_payment.html', context)



def admin_project(request):
    if not request.session.get('admin'):
        return redirect('admin_login')
    
    project = ClientPostProject.objects.select_related('client').all()
    admin_email = request.session.get('admin')

    context ={
        'project' : project,
        'admin_email' : admin_email,
    }
    return render(request, 'admin_project.html', context)


def admin_delete_project(request, id):
    try:
        # Get the project by ID
        project = ClientPostProject.objects.get(id=id)
    except ClientPostProject.DoesNotExist:
        # If the project doesn't exist, redirect back to the project list page
        return redirect('admin_project')

    # Send email notification to the client before deleting the project
    subject = "Your Project Has Been Deleted"
    message = f"Dear {project.client.first_name},\n\nWe regret to inform you that your project titled '{project.title}' has been deleted from our system. If you have any questions or concerns, please contact support.\n\nBest regards,\nWorkSphere"
    from_email = 'worksphere05@gmail.com'  # Replace with your email address
    recipient_list = [project.client.email]

    # Send the email
    send_mail(subject, message, from_email, recipient_list)

    # Delete the project
    project.delete()

    # Redirect back to the project list page
    return redirect('admin_project')

def admin_notification(request):
    try:
        # Attempt to get the logged-in user from the session
        username = request.session.get('admin')
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
            return redirect('admin_login')

        context = {
            'notifications': notifications,
        }
        return render(request, 'admin_notification.html', context)

    except ValueError:
        return redirect('admin_login')  # Redirect to login if session is invalid or role is missing


def admin_proposal(request):
    return render(request, 'admin_proposal.html')

def admin_header_1(request):
    return render(request, 'admin_header_1.html')

def admin_header_2(request):
    return render(request, 'admin_header_2.html')

def admin_header_3(request):
    return render(request, 'admin_header_3.html')

def generate_report(request):
    return render(request, 'generate_report.html')  # Render the report selection page

def admin_freelancer_bank_details(request):
    if not request.session.get('admin'):
        return redirect('admin_login')
        # Retrieve all freelancer bank details
    bank_details = FreelancerRegisterLogin.objects.all()

    context = {
        'bank_details': bank_details,
    }
    return render(request, 'admin_freelancer_bank_details.html', context)


def generate_pdf(request):
    if request.method == "POST":
        selected_fields = request.POST.getlist('fields')  # Get selected fields
        data = {}

        # Fetch data based on selected fields
        if "client" in selected_fields:
            data['clients'] = ClientRegisterLogin.objects.all()
        if "freelancer" in selected_fields:
            data['freelancers'] = FreelancerRegisterLogin.objects.all()
        if "freelancer_bank" in selected_fields:
            data['freelancer_bank'] = ClientPostProject.objects.all()
        if "contact" in selected_fields:
            data['contacts'] = ClientContact.objects.all()
        if "payment" in selected_fields:
            data['payments'] = Payment.objects.all()
        if "project" in selected_fields:
            data['projects'] = ClientPostProject.objects.all()

        # Render data to the PDF template
        template = get_template("report_template.html")
        html = template.render({"data": data})

        # Generate PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=report.pdf"
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse("Error generating PDF", content_type="text/plain")
        return response

    return HttpResponse("Invalid request", status=400)


def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')
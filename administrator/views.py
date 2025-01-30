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
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = AdminUser.objects.get(email=email, password=password)
            request.session['admin'] = email
            request.session['role'] = 'ADMIN'
            return redirect('admin_dashboard')
            
        except:
            return redirect('admin_login')
    
    return render(request, 'auth/admin_login.html')

def admin_forgot_password(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user = AdminUser.objects.get(email = user_email)

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
            return redirect('admin_verify_otp')
            
    return render(request, 'auth/admin_forgot_password.html')

def admin_verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        if request.session.get('otp') == int(otp):
            return redirect('admin_reset_password')
        else:
            return redirect('admin_verify_otp')
    return render(request, 'auth/admin_verify_otp.html')

def admin_reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user_email = request.session.get('email')
            user = AdminUser.objects.get(email = user_email)
            user.password = password
            user.save()
            return redirect('admin_login')
    return render(request, 'auth/admin_reset_password.html')

def admin_dashboard(request):   
    return render(request, 'admin_dashboard.html')

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
        return redirect('admin_login')

    context = {
        'notifications': notifications,
    }
    return render(request, 'admin_notification.html', context)


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
    request.session['done'] = True
    return redirect('admin_login')
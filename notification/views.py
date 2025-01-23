from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from administrator.models import AdminUser
from staticpage.models import ClientContact
from .models import Notification
from freelancer.models import *
from client.models import *
from payment.models import *
from django.core.mail import send_mail


def dashboard(request):
    # Check if the user is an admin or has a certain role (you can adjust this logic)
    is_admin = request.user.is_staff  # Example, adjust to your custom check
    
    # Get notifications based on whether the user is admin or regular
    if is_admin:
        notifications = Notification.objects.all().order_by('-timestamp')  # Admin sees all notifications
    else:
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')  # Regular user sees their notifications
    
    return render(request, 'dashboard.html', {'notifications': notifications, 'is_admin': is_admin})

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('dashboard')

# Triggered when a client posts a new project
def post_project(request):
    if request.method == "POST":
        # Logic for posting a project
        # Assuming the client is already authenticated and sending the project details
        
        # Create notification for admin and freelancers
        project = ClientPostProject.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            client=request.user.client
        )
        
        # Notify admin and all freelancers
        admin_users = AdminUser.objects.filter(is_staff=True)
        freelancers = FreelancerRegisterLogin.objects.all()

        # Create notifications for admins
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message_type='project_posted',
                message=f"A new project titled '{project.title}' has been posted by {request.user.client.first_name}."
            )
        
        # Create notifications for freelancers
        for freelancer in freelancers:
            Notification.objects.create(
                user=freelancer.user,
                message_type='project_posted',
                message=f"A new project titled '{project.title}' has been posted. Check it out!"
            )
        
        messages.success(request, "Project posted successfully!")
        return redirect('project_list')  # Redirect to the project list or wherever appropriate
    return render(request, 'post_project.html')

# Triggered when a freelancer submits a proposal
def submit_proposal(request, project_id):
    project = FreelancerProposal.objects.get(id=project_id)
    if request.method == "POST":
        # Logic to submit the proposal
        # Assuming the freelancer is authenticated and sending the proposal details
        
        # Notify the client
        Notification.objects.create(
            user=project.client.user,
            message_type='proposal_submitted',
            message=f"A new proposal has been submitted for your project '{project.title}' by {request.user.freelancer.first_name}."
        )

        messages.success(request, "Proposal submitted successfully!")
        return redirect('project_details', project_id=project.id)
    return render(request, 'submit_proposal.html', {'project': project})

# Triggered when a client approves a proposal
def approve_proposal(request, proposal_id):
    proposal = FreelancerProposal.objects.get(id=proposal_id)
    if request.method == "POST":
        # Logic for client to approve the proposal
        proposal.is_approved = True
        proposal.save()

        # Notify the freelancer
        Notification.objects.create(
            user=proposal.freelancer.user,
            message_type='proposal_approved',
            message=f"Your proposal for '{proposal.project.title}' has been approved by the client."
        )

        messages.success(request, "Proposal approved!")
        return redirect('proposal_list')  # Redirect to the list of proposals
    return render(request, 'approve_proposal.html', {'proposal': proposal})

# Triggered when a project submission is received
def submit_project(request, project_id):
    project = ClientPostProject.objects.get(id=project_id)
    if request.method == "POST":
        # Logic for freelancer submitting the project
        project.submission = request.POST['submission']
        project.save()

        # Notify the client
        Notification.objects.create(
            user=project.client.user,
            message_type='submission_received',
            message=f"A submission has been received for your project '{project.title}'."
        )

        messages.success(request, "Project submitted successfully!")
        return redirect('project_details', project_id=project.id)
    return render(request, 'submit_project.html', {'project': project})

# Triggered when a client registers
def client_register(request):
    if request.method == "POST":
        # Logic for registering a client
        # Assuming a successful registration
        client = ClientRegisterLogin.objects.create(
            user=request.user,
            company_name=request.POST['company_name'],
            email=request.POST['email']
        )
        
        # Notify admin
        admin_users = AdminUser.objects.filter(is_staff=True)
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message_type='client_registered',
                message=f"A new client '{client.user.first_name}' has registered."
            )
        
        messages.success(request, "Client registered successfully!")
        return redirect('client_dashboard')
    return render(request, 'client_register.html')

# Triggered when a freelancer registers
def freelancer_register(request):
    if request.method == "POST":
        # Logic for registering a freelancer
        freelancer = FreelancerRegisterLogin.objects.create(
            user=request.user,
            skills=request.POST['skills'],
            email=request.POST['email']
        )
        
        # Notify admin
        admin_users = AdminUser.objects.filter(is_staff=True)
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message_type='freelancer_registered',
                message=f"A new freelancer '{freelancer.user.first_name}' has registered."
            )

        messages.success(request, "Freelancer registered successfully!")
        return redirect('freelancer_dashboard')
    return render(request, 'freelancer_register.html')

# Triggered when a client sends a contact message
def send_contact_message(request):
    if request.method == "POST":
        # Logic for sending a contact message
        contact_message = ClientContact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            message=request.POST['message']
        )
        
        # Notify admin
        admin_users = AdminUser.objects.filter(is_staff=True)
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message_type='contact_message',
                message=f"A new contact message has been received from {contact_message.name}."
            )
        
        messages.success(request, "Your message has been sent!")
        return redirect('contact_page')
    return render(request, 'contact_page.html')

# Triggered when a payment is received
def payment_received(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    if request.method == "POST":
        # Logic for confirming payment received
        payment.status = 'received'
        payment.save()

        # Notify the client and freelancer
        Notification.objects.create(
            user=payment.client.user,
            message_type='payment_received',
            message=f"Payment of {payment.amount} has been received for the project '{payment.project.title}'."
        )
        Notification.objects.create(
            user=payment.freelancer.user,
            message_type='payment_received',
            message=f"Payment of {payment.amount} has been received for your project submission."
        )

        messages.success(request, "Payment received and notifications sent!")
        return redirect('payment_page')
    return render(request, 'payment_page.html')

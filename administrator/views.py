from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from staticpage.models import *
from client.models import *
from freelancer.models import *
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

def admin_delete_contact(request, id):
    contact = ClientContact.objects.get(id=id) 
    contact.delete() 
    return redirect('admin_contact')

def admin_client(request):
    if not request.session.get('admin'):
        return render('admin_login')
    
    client = ClientRegisterLogin.objects.all()
    admin_email = request.session.get('admin')

    context ={
        'client' : client,
        'admin_email' : admin_email,
    }
    return render(request, 'admin_client.html', context)

def admin_delete_client(request, id):
    client = ClientRegisterLogin.objects.get(id=id)
    client.delete()
    return redirect('admin_client')

def admin_freelancer(request):
    if not request.session.get('admin'): 
        return redirect('admin_login') 
    
    freelancer = FreelancerRegisterLogin.objects.all()
    admin_email = request.session.get('admin') 

    context = {
        'freelancer' : freelancer,
        'admin_email' : admin_email,
    }

    return render(request, 'admin_freelancer.html', context)

def freelancer_delete_details(request, id):
    contact = FreelancerRegisterLogin.objects.get(id=id) 
    contact.delete() 
    return redirect('admin_freelancer')


def admin_payment(request):
    return render(request, 'admin_payment.html')

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
    project = ClientPostProject.objects.get(id=id)
    project.delete()
    return redirect('admin_project')

def admin_proposal(request):
    return render(request, 'admin_proposal.html')

def admin_logout(request):
    request.session.flush()
    request.session['done'] = True
    return redirect('admin_login')
from django.shortcuts import render, redirect
from .models import *
from staticpage.models import *
import random
import re
from django.core.mail import send_mail

# Create your views here.

def admin_login(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = AdminUser.objects.get(email=email, password=password)

        if user:
            return redirect('admin_dashboard')
        else:
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
    return render(request, 'admin_contact.html')

def admin_client(request):
    return render(request, 'admin_client.html')

def admin_freelancer(request):
    return render(request, 'admin_freelancer.html')

def admin_payment(request):
    return render(request, 'admin_payment.html')

def admin_project(request):
    return render(request, 'admin_project.html')

def admin_proposal(request):
    return render(request, 'admin_proposal.html')

def admin_logout(request):
    request.session.flush()
    request.session['done'] = True
    return redirect('admin_login')
from django.shortcuts import render

# Create your views here.

def admin_login(request):
    return render(request, 'auth/admin_login.html')

def admin_forgot_password(request):
    return render(request, 'auth/admin_forgot_password.html')

def admin_verify_otp(request):
    return render(request, 'auth/admin_verify_otp.html')

def admin_reset_password(request):
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
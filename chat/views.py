from django.shortcuts import render

# Create your views here.

def client_chatbox(request):
    return render(request, 'client_chatbox.html')

def freelancer_chatbox(request):
    return render(request, 'freelancer_chatbox.html')
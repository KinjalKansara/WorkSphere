from django.shortcuts import get_object_or_404, render
from client.models import *
# Create your views here.

def project_view(request, project_id):
    details = get_object_or_404(ClientPostProject, id=project_id)
    skills = details.skills_required.split(',')  # Assuming skills are stored as a comma-separated string
    
    context = {
        'details' : details,
        'skills' : skills,
    }
    return render(request, 'project_view.html', context)

def ai_developement(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='ai_developement')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    return render(request, 'ai_development.html', context)

def animation(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='animation')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }

    return render(request, 'animation.html', context)

def business_strategy(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='business_strategy')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }

    return render(request, 'business_strategy.html', context)

def content_creation(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='content_creation')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }

    return render(request, 'content_creation.html', context)

def contract_drafting(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='contract_drafting')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'contract_drafting.html', context)

def graphic_design(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='graphic_design')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'graphic_design.html', context)

def legal_consulting(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='legal_consulting')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'legal_consulting.html', context)

def logo_design(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='logo_design')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'logo_design.html', context)

def machine_learning(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='machine_learning')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'machine_learning.html', context)

def market_research(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='market_research')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'market_research.html', context)

def social_media_marketing(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='social_media_marketing')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'social_media_marketing.html', context)

def software_development(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='software_development')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'software_development.html', context)

def video_editing(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='video_editing')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'video_editing.html', context)

def web_development(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='web_development')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'web_development.html', context)

def music_composition(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='music_composition')  # Filter only Machine Learning projects

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'music_composition.html', context)

def lyric_writting(request):
    query = request.GET.get('q', '')  # Get search query from the GET request
    machine = ClientPostProject.objects.filter(category='lyric_writting') 

    if query:
        machine = machine.filter(title__icontains=query)  # Apply search filter on project titles
    
    context ={
        'machine': machine, 
        'query': query
    }
    
    return render(request, 'lyric_writting.html', context)
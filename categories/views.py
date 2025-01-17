from django.shortcuts import get_object_or_404, render
from client.models import *
# Create your views here.

def project_view(request, project_id):
    project = get_object_or_404(ClientPostProject, id=project_id)
    skills = project.skills_required.split(',')
    # Get the client from the project
    client = project.client
    location = client.location

    context = {
        'project': project,
        'client': client, 
        'skill' : skills, 
        'location' : location, 
    }
    return render(request, 'project_view.html', context)

def ai_developement(request):
    category = ClientPostProject.objects.filter(category = 'ai_developement')
    
    context ={
        'ai' : category
    }
    return render(request, 'ai_development.html', context)

def animation(request):
    category = ClientPostProject.objects.filter(category = 'animation')
    
    context ={
        'anim' : category
    }
    return render(request, 'animation.html', context)

def business_strategy(request):
    category = ClientPostProject.objects.filter(category = 'business_strategy')
    
    context ={
        'business' : category
    }

    return render(request, 'business_strategy.html', context)

def content_creation(request):
    category = ClientPostProject.objects.filter(category = 'content_creation')
    
    context ={
        'content' : category
    }

    return render(request, 'content_creation.html', context)

def contract_drafting(request):
    category = ClientPostProject.objects.filter(category = 'contract_drafting')
    
    context ={
        'contract' : category
    }
    
    return render(request, 'contract_drafting.html', context)

def graphic_design(request):
    category = ClientPostProject.objects.filter(category = 'graphic_design')
    
    context ={
        'graphic' : category
    }
    
    return render(request, 'graphic_design.html', context)

def legal_consulting(request):
    category = ClientPostProject.objects.filter(category = 'legal_consulting')
    
    context ={
        'legal' : category
    }
    
    return render(request, 'legal_consulting.html', context)

def logo_design(request):
    category = ClientPostProject.objects.filter(category = 'logo_design')
    
    context ={
        'logo' : category
    }
    
    return render(request, 'logo_design.html', context)

def machine_learning(request):
    category = ClientPostProject.objects.filter(category = 'machine_learning')
    
    context ={
        'machine' : category
    }
    
    return render(request, 'machine_learning.html', context)

def market_research(request):
    category = ClientPostProject.objects.filter(category = 'market_research')
    
    context ={
        'market' : category
    }
    
    return render(request, 'market_research.html', context)

def social_media_marketing(request):
    category = ClientPostProject.objects.filter(category = 'social_media_marketing')
    
    context ={
        'social' : category
    }
    
    return render(request, 'social_media_marketing.html', context)

def software_development(request):
    category = ClientPostProject.objects.filter(category = 'software_development')
    
    context ={
        'software' : category
    }
    
    return render(request, 'software_development.html', context)

def video_editing(request):
    category = ClientPostProject.objects.filter(category = 'video_editing')
    
    context ={
        'video' : category
    }
    
    return render(request, 'video_editing.html', context)

def web_development(request):
    category = ClientPostProject.objects.filter(category = 'web_development')
    
    context ={
        'web' : category
    }
    
    return render(request, 'web_development.html', context)

def music_composition(request):
    category = ClientPostProject.objects.filter(category = 'music_composition')
    
    context ={
        'music' : category
    }
    
    return render(request, 'music_composition.html', context)

def lyric_writting(request):
    category = ClientPostProject.objects.filter(category = 'lyric_writting')
    
    context ={
        'lyric' : category
    }
    
    return render(request, 'lyric_writting.html', context)
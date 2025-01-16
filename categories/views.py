from django.shortcuts import render
from client.models import *
# Create your views here.

def project_view(request, project_id):
    project = ClientPostProject.objects.all(id=project_id)

    context ={
        'project' : project
    }
    return render(request, 'project_view.html', context)

def ai_developement(request):
    category1 = ClientPostProject.objects.filter(category = 'ai_development')
    
    context ={
        'ai' : category1
    }
    return render(request, 'ai_development.html', context)

def animation(request):
    return render(request, 'animation.html')

def business_strategy(request):
    return render(request, 'business_strategy.html')

def content_creation(request):
    return render(request, 'content_creation.html')

def contract_drafting(request):
    return render(request, 'contract_drafting.html')

def graphic_design(request):
    return render(request, 'graphic_design.html')

def legal_consulting(request):
    return render(request, 'legal_consulting.html')

def logo_design(request):
    return render(request, 'logo_design.html')

def machine_learning(request):
    return render(request, 'machine_learning.html')

def market_research(request):
    return render(request, 'market_research.html')

def social_media_marketing(request):
    return render(request, 'social_media_marketing.html')

def software_development(request):
    return render(request, 'software_development.html')

def video_editing(request):
    return render(request, 'video_editing.html')

def web_development(request):
    return render(request, 'web_development.html')

def music_composition(request):
    return render(request, 'music_composition.html')

def lyric_writting(request):
    return render(request, 'lyric_writting.html')
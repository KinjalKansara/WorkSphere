from django.urls import path
from . import views

urlpatterns = [
    path('ai_developement/', views.ai_developement, name='ai_developement'),
    path('animation/', views.animation, name='animation'),
    path('business_strategy/', views.business_strategy, name='business_strategy'),
    path('content_creation/', views.content_creation, name='content_creation'),
    path('contract_drafting/', views.contract_drafting, name='contract_drafting'),
    path('graphic_design/', views.graphic_design, name='graphic_design'),
    path('legal_consulting/', views.legal_consulting, name='legal_consulting'),
    path('logo_design/', views.logo_design, name='logo_design'),
    path('machine_learning/', views.machine_learning, name='machine_learning'),
    path('market_research/', views.market_research, name='market_research'),
    path('social_media_marketing/', views.social_media_marketing, name='social_media_marketing'),
    path('software_development/', views.software_development, name='software_development'),
    path('video_editing/', views.video_editing, name='video_editing'),
    path('web_development/', views.web_development, name='web_development'),
    path('music_composition/', views.music_composition, name='music_composition'),
    path('lyric_writting/', views.lyric_writting, name='lyric_writting'),
    path('project_view/<int:project_id>', views.project_view, name='project_view'),
]
from django.db import models


class ClientRegisterLogin(models.Model):
    profile_photo = models.ImageField(upload_to='profile_photos/')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True)
    bio = models.TextField(null=True, max_length=1000)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ClientPostProject(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('intermediate', 'Intermediate Level'),
        ('expert', 'Expert Level'),
    ]

    BUDGET_TYPE_CHOICES = [
        ('fixed', 'Fixed Price'),
        ('hourly', 'Hourly'),
    ]

    CATEGORY_CHOICES = [
        ('ai_developement', 'AI Development'),
        ('animation', 'Animation'),
        ('business_strategy', 'Business Strategy'),
        ('content_creation', 'Content Creation'),
        ('contract_drafting', 'Contract Drafting'),
        ('graphic_design', 'Graphic Design'),
        ('legal_consulting', 'Legal Consulting'),
        ('logo_design', 'Logo Design'),
        ('machine_learning', 'Machine Learning'),
        ('market_research', 'Market Research'),
        ('social_media_marketing', 'Social Media Marketing'),
        ('software_development', 'Software Development'),
        ('video_editing', 'Video Editing'),
        ('web_development', 'Web Development'),
        ('music_composition', 'Music Composition'),
        ('lyric_writting', 'Lyric Writing'),
    ]

    client = models.ForeignKey(ClientRegisterLogin, on_delete=models.CASCADE, related_name='projects', null=True)
    title = models.CharField(max_length=255, help_text="Title of the project")
    description = models.TextField(help_text="Detailed description of the project")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, help_text="Project category")
    budget = models.DecimalField(max_digits=20, decimal_places=2, help_text="Project budget (fixed or hourly)")
    budget_type = models.CharField(max_length=10, choices=BUDGET_TYPE_CHOICES, help_text="Budget type")
    deadline = models.DateField(help_text="Deadline for project completion")
    skills_required = models.CharField(max_length=255, help_text="Skills required for the project")
    attachments = models.FileField(upload_to="project_attachments/", blank=True, null=True, help_text="Project-related files")
    photo = models.ImageField(upload_to="project_photos/", blank=True, null=True, help_text="Project-related photo")
    experience_level = models.CharField(max_length=15, choices=EXPERIENCE_LEVEL_CHOICES, help_text="Required experience level for freelancers")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Time when the project was posted")
    status = models.CharField(max_length=10, null=True)

    def get_skills_list(self):
        return [skill.strip() for skill in self.skills_required.split(",") if skill.strip()]

    def __str__(self):
        return self.title




from django.db import models
from django.utils import timezone

class TeamMember(models.Model):
    """Model for team members"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    diploma = models.CharField(max_length=200)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    department = models.CharField(max_length=100, choices=[
        ('leadership', 'Leadership'),
        ('data_science', 'Data Science'),
        ('urban_planning', 'Urban Planning'),
        ('investment', 'Investment Analysis'),
        ('sustainability', 'Sustainability'),
    ])
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
    class Meta:
        ordering = ['department', 'order']

class ContactMessage(models.Model):
    """Model for contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    interest = models.CharField(max_length=100, choices=[
        ('data_insights', 'Data Insights & Analytics'),
        ('investment', 'Investment Opportunities'),
        ('hazard_analysis', 'Hazard Analysis & Sustainability'),
        ('consulting', 'Consulting Services'),
        ('partnership', 'Partnership Opportunities'),
        ('other', 'Other'),
    ])
    newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.subject} from {self.name}"
    
    class Meta:
        ordering = ['-created_at']

class Contribution(models.Model):
    """Model for recent contributions and publications"""
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=[
        ('journal', 'Journal Publication'),
        ('book', 'Book Chapter'),
        ('white_paper', 'White Paper'),
        ('report', 'Report'),
        ('presentation', 'Presentation'),
    ])
    publication = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    author = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='contributions/', blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']

class Collaboration(models.Model):
    """Model for collaborations and partnerships"""
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='collaborations/')
    description = models.TextField()
    focus_areas = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-start_date']

class Achievement(models.Model):
    """Model for company achievements and awards"""
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=[
        ('award', 'Award'),
        ('recognition', 'Recognition'),
        ('grant', 'Grant'),
        ('patent', 'Patent'),
    ])
    organization = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']

class Service(models.Model):
    """Model for services offered"""
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=100)
    short_description = models.TextField()
    features = models.TextField()
    url = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']

class Testimonial(models.Model):
    """Model for client testimonials"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    testimonial = models.TextField()
    image = models.ImageField(upload_to='testimonials/')
    rating = models.IntegerField(default=5)
    
    def __str__(self):
        return f"{self.name} from {self.company}"
    
    class Meta:
        ordering = ['-id']

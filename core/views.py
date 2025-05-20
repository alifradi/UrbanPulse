from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, 'core/home.html')

def insights(request):
    return render(request, 'core/insights.html')

def investment(request):
    return render(request, 'core/investment.html')

def hazards(request):
    return render(request, 'core/hazards.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Email content
        email_subject = f"UrbanPulse Contact: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        # Send email
        try:
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['contact@urbanpulse.example.com'],  # Replace with actual email in production
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent. We will contact you soon!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'core/contact.html')

def team(request):
    return render(request, 'core/team.html')

def use_cases(request):
    return render(request, 'core/use_cases.html')

def contributions(request):
    return render(request, 'core/contributions.html')

def services(request):
    return render(request, 'core/services.html')

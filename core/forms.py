from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Form for contact messages"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'interest', 'newsletter']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
            'interest': forms.Select(attrs={'class': 'form-select'}),
            'newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

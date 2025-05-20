from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('insights/', views.insights, name='insights'),
    path('investment/', views.investment, name='investment'),
    path('hazards/', views.hazards, name='hazards'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),
    path('use-cases/', views.use_cases, name='use_cases'),
    path('contributions/', views.contributions, name='contributions'),
    path('services/', views.services, name='services'),
]

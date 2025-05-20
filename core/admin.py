from django.contrib import admin
from .models import TeamMember, ContactMessage, Contribution, Collaboration, Achievement, Service, Testimonial

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'department', 'order')
    list_filter = ('department',)
    search_fields = ('name', 'position', 'bio')
    ordering = ('department', 'order')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'interest', 'created_at', 'is_read')
    list_filter = ('interest', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    actions = ['mark_as_read']

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'date')
    list_filter = ('type', 'date')
    search_fields = ('title', 'description', 'author__name')
    date_hierarchy = 'date'

@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('name', 'focus_areas', 'start_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description', 'focus_areas')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'organization', 'date')
    list_filter = ('type', 'date')
    search_fields = ('title', 'description', 'organization')
    date_hierarchy = 'date'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'short_description', 'features')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating')
    list_filter = ('rating',)
    search_fields = ('name', 'company', 'testimonial')

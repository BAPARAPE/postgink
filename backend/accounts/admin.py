from django.contrib import admin
from .models import UserProfile
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_title', 'industry', 'preferred_tone', 'created_at']
    search_fields = [ 'user__username', 'job_title', 'industry']
    
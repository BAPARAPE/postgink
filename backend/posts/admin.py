from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'tone', 'status', 'scheduled_at', 'created_at']
    list_filter = ['status', 'tone']
    search_fields = ['user__username', 'subject', 'content']
    
    
    
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    job_title = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    interests = models.TextField(blank=True)
    preferred_tone = models.CharField(
        max_length=20, 
        choices=[
            ('professional', 'Professionnel'),
            ('storytelling', 'Storytelling'),
            ('hot_take', 'Hot Take'),
        ],
        default='professional'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Profil de {self.user.username}"
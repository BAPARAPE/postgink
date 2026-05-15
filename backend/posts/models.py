from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('scheduled', 'Programmé'),
        ('validated', 'Validé'),
        ('published', 'Publié'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    subject = models.CharField(max_length=200)
    content = models.TextField()
    tone = models.CharField(
        max_length=20,
        choices=[
            ('professional', 'Professionnel'),
            ('storytelling', 'Storytelling'),
            ('hot_take', 'Hot Take'),
        ],
        default='professional'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject[:50]}"

    class Meta:
        ordering = ['-created_at']
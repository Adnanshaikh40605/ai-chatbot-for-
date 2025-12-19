from django.db import models
from django.contrib.auth.models import User


class Persona(models.Model):
    """AI Persona configuration for each user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='persona')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)  # girlfriend, boyfriend, friend, etc.
    personality = models.TextField()  # caring, romantic, playful, etc.
    tone = models.CharField(max_length=50)  # sweet, playful, caring, etc.
    likes = models.TextField(blank=True, null=True)
    dislikes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        verbose_name_plural = "Personas"


class Message(models.Model):
    """Chat message history"""
    SENDER_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}"

    class Meta:
        ordering = ['created_at']


class Memory(models.Model):
    """User preferences and memories for personalization"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    key = models.CharField(max_length=100)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.key}"

    class Meta:
        verbose_name_plural = "Memories"
        unique_together = ['user', 'key']

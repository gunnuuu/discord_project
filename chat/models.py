from django.db import models

# Create your models here.

class DiscordMessage(models.Model):
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'discord_messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.content[:50]}... ({self.created_at})"

class ReceivedMessage(models.Model):
    username = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)
    received_at = models.DateTimeField(auto_now_add=True)
    channel_id = models.CharField(max_length=20, blank=True, null=True)
    message_id = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        db_table = 'received_messages'
        ordering = ['-received_at']
    
    def __str__(self):
        return f"{self.username}: {self.content[:50]}... ({self.received_at})"

from django.contrib import admin
from .models import DiscordMessage, ReceivedMessage

@admin.register(DiscordMessage)
class DiscordMessageAdmin(admin.ModelAdmin):
    list_display = ['content', 'created_at', 'is_sent']
    list_filter = ['is_sent', 'created_at']
    search_fields = ['content']
    readonly_fields = ['created_at']

@admin.register(ReceivedMessage)
class ReceivedMessageAdmin(admin.ModelAdmin):
    list_display = ['username', 'content', 'received_at', 'channel_id']
    list_filter = ['received_at', 'username']
    search_fields = ['username', 'content']
    readonly_fields = ['received_at']

from rest_framework import serializers
from .models import DiscordMessage, ReceivedMessage

class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)

class DiscordMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordMessage
        fields = ['id', 'content', 'created_at', 'is_sent', 'error_message']

class ReceivedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivedMessage
        fields = ['id', 'username', 'content', 'received_at', 'channel_id', 'message_id']

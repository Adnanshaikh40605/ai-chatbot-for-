from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Persona, Message, Memory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PersonaSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Persona
        fields = ['id', 'user_id', 'name', 'role', 'personality', 'tone', 'likes', 'dislikes', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        
        # Update or create persona
        persona, created = Persona.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        return persona


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'sender', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    message = serializers.CharField()


class ChatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'user', 'key', 'value', 'created_at']
        read_only_fields = ['id', 'created_at']

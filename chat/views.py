from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Persona, Message, Memory
from .serializers import (
    PersonaSerializer, MessageSerializer, ChatRequestSerializer,
    ChatResponseSerializer, UserSerializer
)
from .gemini_service import GeminiService


class UserViewSet(viewsets.ViewSet):
    """Simple user creation endpoint"""
    
    def create(self, request):
        # Create anonymous user
        user = User.objects.create_user(
            username=f"user_{User.objects.count() + 1}"
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PersonaViewSet(viewsets.ModelViewSet):
    """CRUD operations for Personas"""
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    
    def retrieve(self, request, pk=None):
        """Get persona by user_id"""
        try:
            persona = Persona.objects.get(user_id=pk)
            serializer = self.get_serializer(persona)
            return Response(serializer.data)
        except Persona.DoesNotExist:
            return Response(
                {"detail": "Persona not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class ChatViewSet(viewsets.ViewSet):
    """Handle chat interactions"""
    
    def create(self, request):
        """Send a chat message and get AI response"""
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = serializer.validated_data['user_id']
        user_message = serializer.validated_data['message']
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get AI response
        gemini_service = GeminiService()
        ai_reply = gemini_service.chat(user, user_message)
        
        response_serializer = ChatResponseSerializer({"reply": ai_reply})
        return Response(response_serializer.data)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """Retrieve chat history"""
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Message.objects.filter(user_id=user_id).order_by('created_at')
    
    def list(self, request, user_id=None):
        """Get chat history for a user"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Format for frontend
        formatted_messages = [
            {
                "id": msg['id'],
                "sender": msg['sender'],
                "message": msg['message'],
                "created_at": msg['created_at']
            }
            for msg in serializer.data
        ]
        
        return Response(formatted_messages)

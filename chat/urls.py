from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'personas', views.PersonaViewSet, basename='persona')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'chat', views.ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
    path('messages/<int:user_id>/', views.MessageViewSet.as_view({'get': 'list'}), name='message-history'),
]

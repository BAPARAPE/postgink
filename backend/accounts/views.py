from rest_framework import generics, permissions 
from rest_framework.response import Response 
from rest_framework.views import APIView 
from django.contrib.auth.models import User 
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer
from .models import UserProfile


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated] 
    
    def patch(self, request):
        profile = request.user.profile 
        serializer = UserProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
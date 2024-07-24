from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import serializers
# Create your views here.
from rest_framework import generics 
from rest_framework.response import Response
from rest_framework import status 
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed


class RegisterView(generics.CreateAPIView): 
    queryset = get_user_model().objects.all() 
    serializer_class = UserSerializer 
    
    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)

class LoginView(generics.CreateAPIView): 
    serializer_class = LoginSerializer 
    
    def post(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        try: 
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user'] 
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh), 
            'access': str(refresh.access_token),
            
        }, status=status.HTTP_200_OK)
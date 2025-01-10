from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request,f"Registered Successfully.")
            return Response({
                "message": "User Created Successfully",
                "user":serializer.data
            },status=status.HTTP_201_CREATED)
        
        return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user is None:
                return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

            login(request, user)

            refresh = RefreshToken.for_user(user)

            response = Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)

            access_token_expiry = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            refresh_token_expiry = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            response.set_cookie(
                'access_token', 
                str(refresh.access_token),
                httponly=True, 
                secure=settings.SECURE_COOKIES, 
                samesite='Strict', 
                max_age=access_token_expiry.total_seconds(), 
                expires=(timezone.now() + access_token_expiry).strftime('%a, %d-%b-%Y %H:%M:%S GMT')
            )

            response.set_cookie(
                'refresh_token', 
                str(refresh),
                httponly=True, 
                secure=settings.SECURE_COOKIES, 
                samesite='Strict', 
                max_age=refresh_token_expiry.total_seconds(),
                expires=(timezone.now() + refresh_token_expiry).strftime('%a, %d-%b-%Y %H:%M:%S GMT')
            )

            messages.success(request, 'Logged In Successfully')
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

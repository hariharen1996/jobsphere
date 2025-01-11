from rest_framework.decorators import api_view,throttle_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect,render
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .serializers import PasswordResetEmailSerializer
from .models import CustomUser
from django.template.loader import render_to_string
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .mixins import RedirectAuthenticatedUserMixin
from .permissions import IsUnauthenticated



class RegisterThrottle(UserRateThrottle):
    rate = '5/hour'

@api_view(['POST'])
@throttle_classes([RegisterThrottle])
@permission_classes([IsUnauthenticated])
def register_view(request):
    if request.user.is_authenticated:
        return Response({
            "message": "You are already registered."
        }, status=status.HTTP_403_FORBIDDEN)
    
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
@permission_classes([IsUnauthenticated])
def login_view(request):
    if request.user.is_authenticated:
        return Response({
            "message": "You are already logged in."
        }, status=status.HTTP_403_FORBIDDEN)
    
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


@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        print(f"refresh_token: {refresh_token}")
        
        if not refresh_token:
            return Response({"error": "No refresh token found in cookies"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            print(f"Token created: {token}")
            token.blacklist()
            print("Token blacklisted successfully.")
        except Exception as e:
            print(f"Error blacklisting token: {e}")
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"message": "Logged out successfully"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        logout(request)
        
        return response

    except Exception as e:
        print(f"Error during logout: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(RedirectAuthenticatedUserMixin,APIView):
    template_name = 'users/password_reset.html'

    def get(self,request):
        if request.user.is_authenticated:
            return redirect('job_home')
      
        return render(request,self.template_name)
    
    def post(self,request):
        if request.user.is_authenticated:
            return redirect('job_home') 
        serializer = PasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(str(user.pk).encode())

                reset_url = reverse('password_reset_confirm_api', kwargs={'uidb64': uidb64, 'token': token})
                print(reset_url)
                full_url = f'http://127.0.0.1:8000/{reset_url}'
                
                subject = "Password Reset Request"
                message = render_to_string('users/password_reset_email.html', {
                    'reset_url': full_url,
                    'user_email': user.email,
                })
                print(full_url)

                
                send_mail(subject,'', settings.EMAIL_HOST_USER, [user.email],html_message=message)
                return redirect('password_reset_done_api')
            except CustomUser.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
                return redirect('password_reset_api') 
            
        return JsonResponse(serializer.errors, status=400)


class PasswordResetDoneView(RedirectAuthenticatedUserMixin,APIView):
    template_name = 'users/password_reset_done.html'

    def get(self,request):
        return render(request,self.template_name)
    
class PasswordResetConfirmView(RedirectAuthenticatedUserMixin,APIView):
    template_name = 'users/password_reset_confirm.html'

    def get(self,request,uidb64,token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk = uid)
            if default_token_generator.check_token(user,token):
                return render(request,self.template_name,{'uidb64':uidb64,'token':token}) 
            else:
                messages.error(request, 'Invalid or expired link.')
                return redirect('password_reset_api') 
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
                messages.error(request, 'Invalid or expired link.')
                return redirect('password_reset_api') 


    def post(self,request,uidb64,token):  
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)

            if default_token_generator.check_token(user,token):
                password = request.data.get('password')
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been successfully reset.')
                return redirect('password_reset_complete_api')
            else:
                messages.error(request, 'Invalid or expired token.')
                return redirect('password_reset_api')
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
                messages.error(request, 'Invalid or expired link.')
                return redirect('password_reset')

class PasswordResetCompleteView(RedirectAuthenticatedUserMixin,APIView):
    def get(self,request):
        return render(request,'users/password_reset_complete.html')    
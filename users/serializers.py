from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import re

class CustomUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'password1', 'password2']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        username = attrs.get('username')
        email = attrs.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})

        if len(username) < 3:
            raise serializers.ValidationError({'username': 'Enter a valid username (at least 3 characters).'})
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username already exists.'})

        if password1 != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        if not re.search(r'[A-Z]', password1):
            raise serializers.ValidationError({'password': 'Password must contain at least one uppercase letter.'})
        if not re.search(r'[0-9]', password1):
            raise serializers.ValidationError({'password': 'Password must contain at least one digit.'})
        if not re.search(r'[@#$!%*?&^()]', password1):
            raise serializers.ValidationError({'password': 'Password must contain at least one special character.'})
        if not re.search(r'[a-z]', password1):
            raise serializers.ValidationError({'password': 'Password must contain at least one lowercase letter.'})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=validated_data['user_type'],
            password=validated_data['password1'],
        )
        return user

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=254)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['username','password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username,password=password)
        if user is None:
            serializers.ValidationError('Invalid username or password')
        attrs['user'] = user
        return attrs 


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
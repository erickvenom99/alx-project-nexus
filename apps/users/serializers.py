from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile
from django.contrib.auth import get_user_model, authenticate

User = get_user_model() 

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'avatar_url', 'bio']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'profile', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(password=password, **validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer to include user data in login response.
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        data['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'profile': {
                'first_name': user.profile.first_name,
                'last_name': user.profile.last_name,
                'avatar_url': user.profile.avatar_url,
                'bio': user.profile.bio,
            }
        }


        return data
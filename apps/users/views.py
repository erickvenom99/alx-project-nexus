from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,  CustomTokenObtainPairSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    API END POINT ALLOW USERS TO REGISTER A NEW ACCOUNT
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                'message': 'User created successfuly, you can now login',
                 'user':serializer.data,
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(TokenObtainPairView):
    """
    JWT Login endpoint (email + password).
    """
    serializer_class = CustomTokenObtainPairSerializer



# Create your views here.

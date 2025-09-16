from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    """
    permission_classes = [permissions.AllowAny] =>
    This allows anyone (even unauthenticated users) to access this endpoint.
    It makes sense because new users need to register without being logged in.
    """
    
class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        The post method is defined to handle incoming POST requests.
        It’s where the login logic is implemented.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        """
        Extracts the username and password from the request body sent by the client.
        """
        
        user = authenticate(request, username=username, password=password)
        """
        Uses Django’s built-in authenticate() function to verify if the credentials are correct.
        If the username and password match, it returns a User object; otherwise, it returns None.
        """
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username
            })
        """
        If the credentials are valid:
            It creates a refresh token using RefreshToken.for_user(user).
            It returns the access token, refresh token, and the username as a JSON response.
            These tokens are used by the client to authenticate future requests.
        """
        
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)


class TokenRefreshView(SimpleJWTTokenRefreshView):
    permission_classes = [permissions.AllowAny]

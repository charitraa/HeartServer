
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, authenticate
from HeartServer.permission import LoginRequiredPermission
from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()


class LoginView(TokenObtainPairView):
    """
    Custom login view that supports authentication via email or username.
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"message": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = authenticate(email=email, password=password)

            if user is not None:
                
                refresh = RefreshToken.for_user(user)
                user_serializer = UserSerializer(user)
                response = Response({
                    'message': 'Login successful',
                    'data': user_serializer.data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=status.HTTP_200_OK)

                response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,
                secure=True,  # Must be True in production
                samesite="None"  # Only use "None" when `secure=True`
                )
                return response
        except User.DoesNotExist:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserMeView(APIView):
    permission_classes = [LoginRequiredPermission]
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
# class UserDetailsByIDView(APIView):
#     permission_classes = [LoginRequiredPermission, IsAdminUser]
#     def get(self, request, user_id, *args, **kwargs):
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

# class UserUpdateView(generics.UpdateAPIView):
#     queryset = User.objects.all()  
#     serializer_class = UserUpdateSerializer
#     permission_classes = [LoginRequiredPermission, IsAdminUser]

#     def get_object(self):
#         return self.request.user
    
class CreateUserView(APIView):
    """
    View for user registration.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

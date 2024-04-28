from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from .models import User

class UserRegistration(APIView):

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        data = request.data 
        mobile = data.get('mobile')
        password = data.get('password')
        try:            
            user = User.objects.get(mobile = mobile)
            if not user.check_password(password):
                raise ValueError('Invalid user & password combination')
            authenticate(request, email=user.email, password=password)              
            # Get or create a new token and return
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key})
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class ForgetPasswordView(APIView):

    def post(self, request):
        data = request.data
        mobile = data.get('mobile')
        password = data.get('new_password')       

        try:            
            user = User.objects.get(mobile = mobile)
            validate_password(password, user=user)
        except Exception as e:
            # If password validation fails, return the error message
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # If password is valid, set and save the password
        user.set_password(password) 
        user.save()

        return Response({'Success': "Password Updated Successfully"})


class LogoutView(APIView):    
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)        
        # Delete the token
        token.delete()                
        # request.session.flush()
        return Response({'success': 'Logout successful'})     


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk = None):
        try:
            user = request.user
            if pk:
                user = User.objects.get(id = pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
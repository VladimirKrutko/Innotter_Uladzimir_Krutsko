from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import boto3

from .serializers import LoginSerializer, UserRegistration
from .renderers import UserJSONRenderer
from django.conf import settings


class RegistrationAPIView(APIView):
    """
    Class that realize functionality for register new user
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistration
    renderer_classes = (UserJSONRenderer,)
    
    def post(self, request):
        """
        Realize user registration
        Args:
            request (json): requset with user data for registration

        Returns:
            user data , status code 
        """
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class LoginAPIView(APIView):
    """
    Class that realize log in operation for user
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UploadImageAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, requset):
        """_summary_

        Args:
            requset (_type_): _description_
        """
        image = requset.FILE['upload']
        user = requset.data.get('email')
        image_link =  settings.AWS_BASE_STORAGE+image.name+'-'+user
        s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket =  s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        bucket.put_object(Key=image_link, Body=image)
        
        return Response(image_link, status=status.HTTP_200_OK)
        
        
        
        
        
        
        
            
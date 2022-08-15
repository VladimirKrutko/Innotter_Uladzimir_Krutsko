from rest_framework import serializers
from django.contrib.auth import authenticate
<<<<<<< HEAD
from user.models import User
from page.serializers import PageSerializer
=======
from .models import User, UploadImage
from page.serializers import PageSerializer
import uuid
>>>>>>> _26.07.2022_Working_with_page_model


class UserSerializer(serializers.ModelSerializer):
    """
    Class for registration new users in system
    """
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        """
        Validate data before create user
        """
        if not data['email']:
            raise serializers.ValidationError('Please input email')

        if not data['password']:
            raise serializers.ValidationError('Please input password')

        return data

    def create(self, validated_data):
        page_ser = PageSerializer()
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        page_data = {'owner': user,
                     'name': user.username,
                     'uuid': str(uuid.uuid4())}
        page_ser.create(validated_data=page_data)
        return user

    def update(self, instance, validated_data):
        if not authenticate(username=validated_data['email'],
                            password=validated_data['password']):
            raise serializers.ValidationError('input incorrect data for user')

        instance.image_s3_path = validated_data['image_s3_path']
        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        print(data)
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)
        print(user)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
        }
<<<<<<< HEAD
=======


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'image_s3_path', 'username', 'password')

    def update(self, instance, validated_data):
        for field in validated_data.keys():
            if validated_data[field] != instance[field]:
                instance[field] = validated_data[field]
        instance.save()
        return instance

>>>>>>> _26.07.2022_Working_with_page_model

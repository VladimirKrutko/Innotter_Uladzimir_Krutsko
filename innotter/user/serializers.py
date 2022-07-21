from rest_framework import serializers
from django.contrib.auth import authenticate
from user.models import User
from page.serializers import PageSerializer


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
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        page_data = {'owner': user.id,
                     'name': user.username}
        PageSerializer(data=page_data)

        return user

    def update(self, instance, validated_data):
        if not authenticate(username=validated_data['email'],
                            password=validated_data['password']):
            raise serializers.ValidationError('input incorrect data for user')

        instance.image_s3_path = validated_data['image_s3_path']
        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    """
    Realise log in process

    Raises:
        serializers.ValidationError: raise this exception if some user data is not valid
    """
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

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
            'username': user.title,
            'token': user.token
        }



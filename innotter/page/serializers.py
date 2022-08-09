from rest_framework import serializers
from page.models import Page, Tag
from user.models import User
from rest_framework.serializers import ValidationError


class PageSerializer(serializers.ModelSerializer):
    """
    Class for serialize Page object
    """

    class Meta:
        model = Page
        fields = ['name', 'description', 'uuid', 'owner']
        read_only_fields = ('owner',)

    def validate(self, data):
        if not User.objects.get(id=data['owner']):
            raise ValidationError('this user is not exist in model')

    def create(self, validated_data):
        page = Page(**validated_data)
        print('create_page')
        page.save()
        return page

    def update(self, instance, validated_data):
        update_fields = set([f.name for f in instance._meta.get_fileds()]) & set(validated_data.keys())
        for field in update_fields:
            setattr(instance, field, validated_data[field])

        instance.save()

        return instance


class PagePublicSerializer(serializers.Serializer):
    """
    Serialize for public user
    """
    followers = serializers.ListField(
        child=serializers.DictField())

    def validate(self, data):
        validate_data = [User.objects.get(email=user.get('email')).id
                         for user in data.get('followers')]
        return {'followers': validate_data}

    def update(self, instance, validated_data):
        for user_id in validated_data.get('followers'):
            instance.followers.add(user_id)
        instance.save()
        return instance


class PagePrivateSerializer(serializers.Serializer):
    """
    Serialize for private user
    """
    followers = serializers.ListField(
        child=serializers.DictField())
    follow_requests = serializers.ListField(
        child=serializers.DictField())

    def validate(self, data):
        validate_data = {}
        if data.get('followers'):
            validate_data['followers'] = [User.objects.get(email=user.get('email')).id
                                          for user in data.get('followers')]

        elif data.get('follow_requests'):
            validate_data['follow_requests'] = [User.objects.get(email=user.get('email')).id
                                                for user in data.get('follow_requests')]

        return validate_data

    def update(self, instance, validated_data):

        if validated_data.get('followers'):
            for user_id in validated_data.get('followers'):
                instance.followers.add(user_id)

        elif validated_data.get('follow_requests'):
            for user_id in validated_data.get('follow_requests'):
                instance.follow_requests.add(user_id)

        instance.save()

        return instance


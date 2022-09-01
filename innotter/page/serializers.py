from datetime import datetime

from user.models import User
from page.models import Page, Tag

from rest_framework import serializers
from django.core import serializers as django_ser
from rest_framework.serializers import ValidationError


class PageSerializer(serializers.ModelSerializer):
    """
    Class for serialize Page object
    """

    class Meta:
        model = Page
        fields = ['name', 'description', 'uuid', 'owner', 'unblock_date']
        read_only_fields = ('owner',)

    def validate(self, data):

        if data.get('tag') is not None:
            if Tag.objects.filter(name=data['tag']):
                data['tag'] = Tag.objects.get(name=data['tag'])
            else:
                tag = Tag(name=data['tag'])
                tag.save()
                data['tag'] = tag

        elif data.get('unblock_date') is not None:
            if data['unblock_date'] < datetime.now():
                raise ValidationError('Incorrect date')
        return data

    def create(self, validated_data):
        page = Page(**validated_data)
        page.save()
        return page

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def serialize_page_post(page_obj, post_obj):
        """
        Method for transform page and post obj to json in format:
        {
        'page': page info,
        'posts': all post from this page
        }
        """
        page_json = django_ser.serialize('json', [page_obj, ])
        post_json = django_ser.serialize('json', [post for post in post_obj])
        result_json = {
            'page': page_json,
            'posts': post_json
        }
        return result_json


class BlockPageSerializer(serializers.Serializer):
    unblock_date = serializers.DateTimeField()

    def validate(self, data):
        if len(data.keys()) > 1:
            raise ValidationError('Incorrect number of fields (only unblock_date)')
        elif data['unblock_date'] < datetime.now():
            raise ValidationError('Incorrect date')
        return data

    def update(self, instance, validated_data):
        instance['unblock_date'] = validated_data['unblock_date']
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
        child=serializers.DictField(), required=False)
    follow_requests = serializers.ListField(
        child=serializers.DictField(), required=False)

    def validate(self, data):
        validate_data = {}
        if data.get('followers'):
            validate_data['followers'] = [User.objects.get(email=user.get('email'))
                                          for user in data.get('followers')]

        elif data.get('follow_requests') is not None:
            validate_data['follow_requests'] = [User.objects.get(email=user.get('email')).id
                                                for user in data.get('follow_requests')]
        elif data.get('unblock_date') is not None:
            raise ValidationError('You can not block page')
        return validate_data

    def update(self, instance, validated_data):

        if validated_data.get('followers'):
            fol_req = list(map(lambda x: x.id, instance.follow_requests.all()))
            for user in validated_data.get('followers'):
                if user.id in fol_req:
                    instance.followers.add(user.id)
                    instance.follow_requests.remove(user)

        elif validated_data.get('follow_requests'):
            for user_id in validated_data.get('follow_requests'):
                instance.follow_requests.add(user_id)
        instance.save()
        return instance

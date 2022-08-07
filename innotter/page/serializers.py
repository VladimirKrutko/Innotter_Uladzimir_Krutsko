from rest_framework import serializers
from page.models import Page, Tag
from user.models import User
from rest_framework.serializers import ValidationError


class PageSerializer(serializers.ModelSerializer):
    """
    Class for serialize Page object
    """
    name = serializers.CharField(max_length=100)
    owner = serializers.IntegerField()

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
        instance.name = validated_data.get('name', instance.name)
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.description = validated_data.get('description', instance.description)
        instance.unblock_date = validated_data.get('unblock_date', None)

        if validated_data.get('tags') is not None:
            tag = Tag.objects.get(name=validated_data.get('tags'))
            instance.tags.add(tag)

        instance.save()
        return instance


class PagePrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['followers', 'follow_requests']

    def update(self, instance, validated_data):

        if validated_data.get('followers') is not None:
            followers = [User.objects.get(email=user.get('email')).id for user in validated_data.get('followers')]
            for user in followers:
                try:
                    instance.follow_requests.get(email=user.email)
                    instance.follow_requests.remove(user)
                    instance.followers.add(user)
                except:
                    raise ValidationError('user did not send a request fro follow')

        elif validated_data.get('follow_requests') is not None:
            follow_req = [User.objects.get(email=user.get('email')).id
                          for user in validated_data.get('follow_requests')]
            for user in follow_req:
                try:
                    instance.follow_requests.add(user)
                except:
                    ValidationError('Can not add to follow request')

        instance.save()
        return instance


class PagePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['followers']

    def update(self, instance, validated_data):
        followers = [User.objects.get(email=user.get('email')).id
                     for user in validated_data.get('followers')]
        for user in followers:
            instance.followers.add(user)

        instance.save()
        return instance

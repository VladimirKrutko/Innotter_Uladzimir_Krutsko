from rest_framework import serializers
from .models import Page, Tag
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
        page.save()
        return page

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.description = validated_data('description', instance.description)
        instance.save()
        return instance


class PageSubscribe(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['follow_requests', 'name', 'owner', 'followers', 'is_private', ]

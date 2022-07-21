from rest_framework import serializers
from .models import Page, Tag
from ..user.models import User
from rest_framework.serializers import ValidationError


class PageSerialize(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    owner = serializers.IntegerField()

    class Meta:
        model = Page
        fields = ['name', 'owner']

    def validate(self, data):
        if not User.objects.get(id=data['owner']):
            raise ValidationError('this user is not exist in model')

    def create(self, validated_data):
        page = Page(**validated_data)
        page.save()
        return page

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.uuid = validated_data['uuid']
        instance.description = validated_data['description']
        instance.save()
        return instance

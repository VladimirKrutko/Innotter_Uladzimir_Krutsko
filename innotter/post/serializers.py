from rest_framework import serializers
from post.models import Post
from rest_framework.serializers import ValidationError


class PostSerialize(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['page_id', 'reply_to', 'content']

    def create(self, validated_data):
        post = Post(**validated_data)
        post.save()
        return post

    def update(self, instance, validated_data):
        if validated_data.get('content') is not None:
            instance.content = validated_data.get('content')
        elif validated_data.get('likes') is not None:
            instance.likes.add(validated_data.get('likes'))
        instance.save()
        return instance

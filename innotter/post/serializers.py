from rest_framework import serializers
from datetime import datetime
from post.models import Post
from user.models import User
from page.models import Page


class PostSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    reply_to = serializers.IntegerField()
    content = serializers.CharField(max_length=10000)
    likes = serializers.ListField(
        child=serializers.DictField())
    is_delete = serializers.BooleanField()
    """
    'likes': [{'email': 'email@gmail.com'},]
    """
    def validate(self, data):
        data['page_id'] = Page.objects.get(owner=data['email']).pk
        del data['email']

        if data['likes']:
            data['likes'] = [User.objects.get(email=email['email']).pk for email in data['likes']]
        return data

    def create(self, validated_data):
        post = Post(**validated_data)
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)

        if validated_data.get('likes') is not None:
            for like in validated_data['likes']:
                instance.likes.add(like)

        instance.update_date = str(datetime.now())
        instance.save()
        return instance

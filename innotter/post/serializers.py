from rest_framework import serializers
from post.models import Post
from datetime import datetime


class PostSerialize(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['page_id', 'reply_to', 'content']

    def validate(self, data):
        print(data)
        return data

    def create(self, validated_data):

        post = Post(**validated_data)
        post.save()

        return post

    def update(self, instance, validated_data):

        instance.content = validated_data.get('content', instance.content)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)

        if validated_data.get('likes') is not None:
            instance.likes.add(validated_data.get('likes'))

        instance.update_date = str(datetime.now())
        instance.save()
        return instance


from rest_framework import serializers
from post.models import Post
from page.models import Page


class PostSerialize(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['page_id', 'reply_to', 'content']

    def validate(self, data):
        print(data)
        return data

    def create(self, validated_data):
        # page = Page.objects.get(id=validated_data['page_id'])

        post = Post(**validated_data)
        # post.page_id = page
        post.save()
        return post

    def update(self, instance, validated_data):
        if validated_data.get('content') is not None:
            instance.content = validated_data.get('content')
        elif validated_data.get('likes') is not None:
            instance.likes.add(validated_data.get('likes'))
        print(validated_data)
        instance.save()
        return instance

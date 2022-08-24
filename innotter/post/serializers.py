from rest_framework import serializers
from datetime import datetime
from post.models import Post
from user.models import User
from page.models import Page


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('page_id', 'reply_to', 'content', 'likes', 'is_delete')

    def validate(self, data):
        data['page_id'] = Page.objects.get(pk=data['page_id'])

        if data.get('reply_to'):
            data['reply_to'] = Post.objects.get(pk=data['reply_to'])
        else:
            data['reply_to'] = Post.objects.get(pk=-1)

        if data.get('likes'):
            data['likes'] = [User.objects.get(email=email['email']) for email in data['likes']]

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


# class PostUpdateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Post
#         fields = ('likes', 'content', 'is_delete')
#
#     def validate(self, data):
#         if data.get('likes'):
#             # data['likes'] = User.objects.filter(email__in=[email for email in data['likes']]).set()
#             data['likes'] = [User.objects.get(email=email['email']) for email in data['likes']]
#         return data
#
#     def update(self, instance, validated_data):
#         instance.content = validated_data.get('content', instance.content)
#         instance.is_delete = validated_data.get('is_delete', instance.is_delete)
#
#         if validated_data.get('likes') is not None:
#             for like in validated_data['likes']:
#                 instance.likes.add(like)
#
#         instance.update_date = str(datetime.now())
#         instance.save()
#         return instance


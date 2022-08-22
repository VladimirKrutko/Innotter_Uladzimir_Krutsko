from rest_framework import serializers
from datetime import datetime
from post.models import Post
from user.models import User
from page.models import Page


class PostSerializer(serializers.Serializer):

    page_id = serializers.IntegerField()
    reply_to = serializers.IntegerField(default=-1, required=False)
    content = serializers.CharField(max_length=10000, required=False)
    likes = serializers.ListField(
        child=serializers.DictField(), required=False)
    is_delete = serializers.BooleanField(default=False, required=False)
    """
    'likes': [{'email': 'email@gmail.com'},]
    """
    def validate(self, data):
        # data['page_id'] = Page.objects.get(pk=data['page_id'])
        # # del data['email']
        if data.get('reply_to'):
            data['reply_to'] = Post.objects.get(pk=data['reply_to'])
        else:
            data['reply_to'] = Post.objects.get(pk=-1)

        if data.get('likes'):
            # data['likes'] = User.objects.filter(email__in=[email for email in data['likes']]).set()
            data['likes'] = [User.objects.get(email=email['email']) for email in data['likes']]
        return data

    def create(self, validated_data):
        print(validated_data)
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

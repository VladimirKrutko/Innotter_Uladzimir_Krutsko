from rest_framework import serializers
from datetime import datetime
from post.models import Post


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('page_id', 'reply_to', 'content', 'likes', 'is_delete')

    def validate(self, data):
        # if data.get('reply_to'):
        #     data['reply_to'] = Post.objects.get(pk=data['reply_to']).pk
        # else:
        #     data['reply_to'] = Post.objects.get(pk=-1).pk
        return data

    def create(self, validated_data):
        post = Post(**validated_data)
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)

        if validated_data.get('likes') is not None:
            if validated_data['likes'][0] in instance.likes.all():
                instance.likes.remove(validated_data['likes'][0])
            else:
                instance.likes.add(validated_data['likes'][0])

        instance.update_date = str(datetime.now())
        instance.save()
        return instance

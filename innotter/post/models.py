from django.db import models

class Post(models.Model):
    """
    Class with page model
    """
    page = models.ForeignKey('page.Page',to_field='uuid',on_delete=models.DO_NOTHING, related_name='posts')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='replies')
    like = models.ManyToManyField('user.User', related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

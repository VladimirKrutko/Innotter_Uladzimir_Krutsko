from django.db import models


class Post(models.Model):

    page_id = models.ForeignKey('page.Page', on_delete=models.PROTECT)
    reply_to = models.ForeignKey('post.Post', on_delete=models.PROTECT, default=-1)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('user.User')
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + '_' + str(self.page_id)


from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Page(models.Model):
    """
    Class with Page model
    """
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='tag')
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='owner')
    followers = models.ManyToManyField('user.User', related_name='follows')
    subscriptions = models.ManyToManyField('user.User', related_name='subscription')
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('user.User', related_name='requests')
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name + ' ' + self.owner

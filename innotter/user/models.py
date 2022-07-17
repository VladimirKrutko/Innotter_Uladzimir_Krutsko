from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    User model in innoter project
    """
    class Roles(models.TextChoices):
        """
        Class with user roles
        """
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    title = models.CharField(max_length=80)
    create_date = models.DateTimeField()
    block_date = models.DateTimeField()
    is_blocked = models.BooleanField(default=False)
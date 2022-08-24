from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, role='user'):
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        user = self.create_user(username, email, password, 'admin')
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model in innotter project
    """

    class Roles(models.TextChoices):
        """
        Class with user roles
        """
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200)
    role = models.CharField(max_length=9, choices=Roles.choices, default='user')
    create_data = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True, default=None)
    unblock_date = models.DateField(default=None, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self) -> models.EmailField:
        return self.email

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from django.db import models
from jsonschema import ValidationError
import jwt
from datetime import datetime, timedelta
from django.conf import settings



class MyUserManager(BaseUserManager):
    
    """
    Class with function for create user and super_user
    """
    
    def create_user(self, email, title, password, role = 'user', **kwargs):
        """
        Base function for create user

        Args:
            email (str): user email
            title (str): user nickname
            password (str): user password

        Returns:
            user object
        """
        
        if email is None:
            raise TypeError('Input user email please')
        
        if password is None:
            raise TypeError('Input password please')
        
        
        
        user = self.model(
            email = self.normalize_email(email),
            title = title,
            role = role,
            **kwargs
            )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, title, password, **kwargs):
        """
        Function for create superuser(admin)

        Args:
            email (str): user email
            title (str): user nickname
            password (str): user password

        Returns:
            user object
        """
        if email is None:
            raise TypeError('Input user email please')
        
        if password is None:
            raise TypeError('Input password please')
        
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        # kwargs.setdefault('is_active', True)
        kwargs.setdefault('role', 'admin')
        
        user = self.create_user(
            email = self.normalize_email(email),
            title = title,
            password = password,
            **kwargs
        )
        user.save()
        
        return user
        

class User(AbstractBaseUser, PermissionsMixin):
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

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    title = models.CharField(max_length=80)
    create_data = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['title']
    
    def __str__(self) -> str:
        return self.email 
    
    def get_role(self) -> str:
        return self.role
        
        
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        
        dt = datetime.now() + timedelta(days=1)
        
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token 


     
    
        
    
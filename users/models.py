from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Manager (BaseUserManager) : 

    def create_user(self,**fields) : 
        password = fields.pop('password')
        user = self.model(**fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser (self,**fields) :
        fields['is_staff'] = True
        fields['is_superuser'] = True
        return self.create_user(**fields)

class User (AbstractUser) :
    objects = Manager()
    username = None
    user_permissions = None

    email = models.EmailField(unique=True)
    picture = models.ImageField(upload_to='user-pics/',default='user.png')
    points = models.IntegerField(default=0)
    full_name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('full_name',)
    

    def __str__(self) -> str:
        return self.full_name
    
    @staticmethod
    def get_leaders ():
        return User.objects.order_by('-points')[:5].values('full_name','points')
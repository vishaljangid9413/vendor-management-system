from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from .manager import UserManager
# Create your models here.


def name_validation(value):
    if not value or not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError("Name must contain only alphabetic characters.")    

def number_validation(value):
    if not value or len(str(value)) != 10:
        raise ValidationError("Mobile number must contain only 10 digits")


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, validators=[name_validation])
    email = models.EmailField(unique=True)
    mobile = models.IntegerField(unique=True, validators=[number_validation])
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ['name', 'email']

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return self.email
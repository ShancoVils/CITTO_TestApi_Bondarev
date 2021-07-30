from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager

OFFICIAL_LIST =(
    ("1", "Уборщик"),
    ("2", "Охранник"),
    ("3", "Кассир"),
)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    FIO = models.CharField(max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=15, blank=True )
    Official = models.CharField(max_length=1, choices = OFFICIAL_LIST)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    token_data = models.CharField(max_length=255,blank=True)
    activate_code = models.CharField(max_length=255,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

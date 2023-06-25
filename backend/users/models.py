from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), max_length=254, unique=True)

    # https://code.djangoproject.com/ticket/20097
    USERNAME_FIELD = 'email'
    AbstractUser.REQUIRED_FIELDS = ['username']

    def clean(self) -> None:
        if self.username == 'me':
            raise ValidationError('uncorrect username')

    def __str__(self) -> str:
        return self.email + " " + self.username

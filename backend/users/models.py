from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        max_length=settings.USER_EMAIL_MAX_LENGTH,
        unique=True
    )

    # https://code.djangoproject.com/ticket/20097
    USERNAME_FIELD = 'email'
    AbstractUser.REQUIRED_FIELDS = ['username']

    def clean(self) -> None:
        if self.username == 'me':
            raise ValidationError('uncorrect username')

    class Meta:
        ordering = ["-id"]
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email + " " + self.username + " " + str(self.pk)

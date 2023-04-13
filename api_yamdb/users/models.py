from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'US'
    MODERATOR = 'MD'
    ADMIN = 'AD'
    ROLE = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(
        max_length=2,
        choices=ROLE,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

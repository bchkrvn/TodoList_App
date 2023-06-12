from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField("email address", blank=False, null=False)
    updated = models.DateTimeField(auto_now=True)

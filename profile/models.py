# coding: utf-8

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ''' User profile'''

    user = models.OneToOneField(User)
    avatar = models.ImageField()

# coding: utf-8

import random
import string
import hashlib
import base64

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class UserAuthCode(object):
    def __init__(self, secret, salt_len=8, hash=hashlib.sha256):
        self.secret = secret
        self.salt_len = salt_len
        self.hash = hash

    def salt(self):
        s = [random.choice(string.letters + string.digits)
             for i in xrange(self.salt_len)]
        return "".join(s)

    def digest(self, user, salt):
        # Use username, email and date_joined to generate digest
        auth_message = ''.join((self.secret, user.username, user.email,
                               str(user.date_joined), salt))
        md = self.hash()
        md.update(auth_message)

        return base64.urlsafe_b64encode(md.digest()).rstrip('=')

    def auth_code(self, user):
        salt = self.salt()
        digest = self.digest(user, salt)

        return "%s%s" % (salt, digest)

    def is_valid(self, user, auth_code):
        #import pdb; pdb.set_trace()
        salt = auth_code[:self.salt_len]
        digest = auth_code[self.salt_len:]

        # CAVEAT: Make sure UserAuthCode cannot be used to reactivate locked
        # profiles.
        if user.last_login >= user.date_joined:
            return False

        return digest == self.digest(user, salt)


class Profile(models.Model):
    ''' User profile'''

    SEX_UNKNOWN = 0
    SEX_MALE = 1
    SEX_FEMALE = 2
    SEX_CHOICES = (
        (SEX_UNKNOWN, _("unknown")),
        (SEX_MALE, _("male")),
        (SEX_FEMALE, _('female'))
    )
    user = models.OneToOneField(User)
    sex = models.SmallIntegerField(
        blank=True, null=True,
        choices=SEX_CHOICES,
        verbose_name=_('sex'))
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name=_('date of birth'))


def activate_user(user, code):
    encoder = UserAuthCode(settings.SECRET_KEY)
    if encoder.is_valid(user, code):
        user.is_active = True
        user.save()
        return True
    return False


def create_new_user(username, password, first_name, last_name, email):
    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_staff=False,
        is_active=True,
    )
    user.set_password(password)
    user.save()
    return user

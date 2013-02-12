# coding: utf-8

import random
import string
import hashlib
import base64

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

    user = models.OneToOneField(User)
#    avatar = models.ImageField()

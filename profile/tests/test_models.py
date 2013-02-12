# coding: utf-8

import unittest

from django.conf import settings
from django.utils import timezone

from challenge.tests.factories import UserFactory
from profile.models import UserAuthCode, activate_user


class UserAuthCodeTest(unittest.TestCase):

    def setUp(self):
        self.encoder = UserAuthCode('secret')
        self.user = UserFactory(is_active=False)

    def tearDown(self):
        self.encoder = None
        self.user.delete()
        self.user = None

    def test_user(self):
        self.assertIsNotNone(self.user.date_joined)
        self.assertTrue(self.user.date_joined >= self.user.last_login)

    def test_salt(self):
        salt = self.encoder.salt()
        self.assertEqual(8, len(salt))

    def test_auth_code(self):
        code = self.encoder.auth_code(self.user)
        self.assertIsNotNone(code)

    def test_complete_activation(self):
        code = self.encoder.auth_code(self.user)
        self.assertTrue(self.encoder.is_valid(self.user, code))

    def test_wrong_key(self):
        self.assertFalse(self.encoder.is_valid(self.user, 'aaa'))

    def test_already_activated(self):
        code = self.encoder.auth_code(self.user)
        self.user.last_login = timezone.now()
        self.user.save()
        self.assertFalse(self.encoder.is_valid(self.user, code))


class TestUserActivation(unittest.TestCase):
    def setUp(self):
        encoder = UserAuthCode(settings.SECRET_KEY)
        self.user = UserFactory(is_active=False)
        self.code = encoder.auth_code(self.user)

    def tearDown(self):
        self.user.delete()
        self.code = None

    def test_user_activation(self):
        self.assertTrue(activate_user(self.user, self.code))
        self.assertTrue(self.user.is_active)

    def test_wrong_code(self):
        self.assertFalse(activate_user(self.user, 'self.code'))
        self.assertFalse(self.user.is_active)

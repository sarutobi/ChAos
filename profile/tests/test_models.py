# coding: utf-8

import unittest

from django.utils import timezone

from challenge.tests.factories import UserFactory
from profile.models import UserAuthCode


class UserAuthCodeTest(unittest.TestCase):

    def setUp(self):
        self.encoder = UserAuthCode('secret')
        self.user = UserFactory()

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

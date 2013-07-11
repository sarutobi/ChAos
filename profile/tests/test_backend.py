# coding: utf-8

import unittest

from django.contrib.auth.models import User

from profile.forms import SignUpForm
from profile.backends import EmailAuthBackend


class EmailBackendTest(unittest.TestCase):

    def setUp(self):
        data = {
            'email': 'test@example.com',
            'password1': 'test',
            'password2': 'test',
            'username': 'dummyuser',
            'first_name': 'First name',
            'last_name': 'Last name',
        }
        form = SignUpForm(data)
        form.is_valid()
        print form.errors
        self.user = form.save()

    def tearDown(self):
        self.user.delete()

    def test_authenticate(self):
        auth = EmailAuthBackend()
        user = auth.authenticate(username='test@example.com', password='test')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)


# coding: utf-8

import unittest

from profile.forms import SignUpForm


class TestSignUpForm(unittest.TestCase):

    def setUp(self):
        self.data = {
            'email': 'test@example.com',
            'password1': 'test',
            'password2': 'test',
            'username': 'dummyuser',
        }

    def tearDown(self):
        self.data = None

    def test_signup_form(self):
        form = SignUpForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid(), form.errors)

    def test_user_creation(self):
        form = SignUpForm(self.data)
        user = form.save()
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.pk)
        user.delete()

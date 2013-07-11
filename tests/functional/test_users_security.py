# coding: utf-8

from django.contrib.auth.models import User

from django_webtest import WebTest

from profile.tests.factories import UserFactory


class test_login(WebTest):
    def setUp(self):
        self.user = UserFactory()

    def tearDown(self):
        self.user.delete()
        self.user = None

    def test_login(self):
        form = self.app.get('/accounts/login/').form
        form['username'] = self.user.email
        form['password'] = '123'
        res = form.submit().follow()
        self.assertEqual(200, res.status_code)


class test_create_user(WebTest):
    def setUp(self):
        self.new_user = UserFactory.build()

    def tearDown(self):
        User.objects.all().delete()

    def test_create_user(self):
        self.assertEqual(0, User.objects.all().count())
        form = self.app.get('/accounts/register/').form
        form['username'] = self.new_user.username
        form['first_name'] = self.new_user.first_name
        form['last_name'] = self.new_user.last_name
        form['email'] = self.new_user.email
        form['password1'] = self.new_user.password
        form['password2'] = self.new_user.password
        res = form.submit().follow()
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, User.objects.all().count())

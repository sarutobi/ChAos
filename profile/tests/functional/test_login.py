# coding: utf-8

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
        res = form.submit()
        self.assertEqual(302, res.status_code)

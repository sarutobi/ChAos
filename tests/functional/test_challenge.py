# coding: utf-8

from django.utils.translation import activate, deactivate
from django_webtest import WebTest

from profile.tests.factories import UserFactory

from challenge.models import Challenge
from challenge.tests.factories import ChallengeFactory


class TestChallengeList(WebTest):
    def setUp(self):
        self.resp = self.app.get('/challenge/')

    def tearDown(self):
        self.resp = None

    def test_challenge_response(self):
        self.assertEqual(200, self.resp.status_code)

    def test_challenge_redirect(self):
        self.assertRedirects(self.app.get('/challenge'), '/challenge/', 301)

    def test_challenge_template(self):
        self.assertTemplateUsed(
            self.resp,
            'challenge_list.html')

    def test_challenge_context(self):
        self.assertIsNotNone(self.resp.context['challenges'])


class TestChallengeFilter(WebTest):
    def setUp(self):
        for x in xrange(100):
            ChallengeFactory()
        self.resp = self.app.get('/challenge/')

    def tearDown(self):
        Challenge.objects.all().delete()

    def test_challenges_count(self):
        self.assertEqual(100, len(self.resp.context['challenges']))


class TestChallengeDetails(WebTest):

    def setUp(self):
        self.challenge = ChallengeFactory()
        self.resp = self.app.get('/challenge/view/%s' % self.challenge.slug)

    def tearDown(self):
        self.challenge.delete()
        self.challenge = None
        self.resp = None

    def test_response(self):
        self.assertEqual(200, self.resp.status_code)


class TestCreateChallenge(WebTest):
    extra_environ = {
        'HTTP_ACCEPT_LANGUAGE': 'ru',
    }

    def setUp(self):
        self.user = UserFactory()
        activate('ru')

    def tearDown(self):
        self.user.delete()
        deactivate()

    def test_without_logo(self):
        before = Challenge.objects.count()
        form = self.app.get('/challenge/create', user=self.user.email).form
        form['title'] = 'Test challenge'
        form['summary'] = 'This is example challenge'
        form['description'] = 'Example challenge that must be deleted'
        form['cause'] = 0
        form['slug'] = 'test_challenge'
        form['start_at'] = '1.9.2012'
        form['end_at'] = '31.5.2013'
        resp = form.submit(user=self.user.email)
        self.assertEqual(302, resp.status_code)
        self.assertEqual(Challenge.objects.count(), before + 1)


class TestUserJoinChallenge(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.first_challenge = ChallengeFactory()
        self.second_challenge = ChallengeFactory()

    def tearDown(self):
        self.first_challenge.delete()
        self.second_challenge.delete()
        self.user.delete()
        self.first_challenge = None
        self.second_challenge = None
        self.user = None

    def test_join_possibility(self):
        page = self.app.get('/challenge/view/%s' % self.first_challenge.slug)
        expect = "/challenge/join/%s" % self.first_challenge.slug
        assert expect in page.text

    def test_join_unregistered(self):
        before = self.first_challenge.users.count()
        page = self.app.get('/challenge/join/%s' % self.first_challenge.slug)
        self.assertEqual(302, page.status_code)
        self.assertEqual(before, self.first_challenge.users.count())

    def test_join_registered(self):
        before = self.first_challenge.users.count()
        page = self.app.get(
            '/challenge/join/%s' % self.first_challenge.slug, user=self.user)
        self.assertEqual(302, page.status_code)
        self.assertEqual(before + 1, self.first_challenge.users.count())



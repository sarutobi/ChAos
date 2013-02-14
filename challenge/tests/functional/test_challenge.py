# coding: utf-8

from django_webtest import WebTest

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
        self.resp = self.app.get('/challenge/%s' % self.challenge.slug)

    def tearDown(self):
        self.challenge.delete()
        self.challenge = None
        self.resp = None

    def test_response(self):
        self.assertEqual(200, self.resp.status_code)


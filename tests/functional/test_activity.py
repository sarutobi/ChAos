# -*- coding: utf-8 -*-

from django_webtest import WebTest

from profile.tests.factories import UserFactory
from challenge.tests.factories import ChallengeFactory, ActivityFactory


class TestCreateActivity(WebTest):
    def setUp(self):
        self.challenge = ChallengeFactory()
        self.user = UserFactory()
        self.activity = ActivityFactory.build()

    def tearDown(self):
        self.activity = None
        self.challenge.delete()
        self.challenge = None
        self.user.delete()
        self.user = None

    def test_createActivity(self):
        before = self.challenge.activity_set.count()
        form = self.app.get('/challenge/appendactivity/%s' % self.challenge.slug, user=self.user).form
        form['title'] = self.activity.title
        form['description'] = self.activity.description
        form['reward'] = self.activity.reward
        form['reward_cost'] = self.activity.reward_cost
        form['reward_cost_type'] = self.activity.reward_cost_type
        res = form.submit(user=self.user).follow()
        self.assertEqual(200, res.status_code)
        self.assertEqual(before + 1, self.challenge.activity_set.count())

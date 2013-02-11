# coding: utf-8

import unittest

from challenge.forms import ChallengeForm, ActivityForm
from .factories import ChallengeFactory, ActivityFactory, UserFactory


class TestChallengeForm(unittest.TestCase):

    def setUp(self):
        self.challenge = ChallengeFactory.attributes()
        self.challenge['creator'] = None

    def tearDown(self):
        self.challenge = None

    def test_form(self):
        form = ChallengeForm(self.challenge)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid(), form.errors)

    def test_save(self):
        self.challenge = ChallengeFactory.attributes()
        user = self.challenge['creator']
        user.save()
        self.challenge['creator'].save()
        form = ChallengeForm(self.challenge)
        form.is_valid()
        form.instance.creator = user
        ch = form.save()
        self.assertIsNotNone(ch.pk)
        ch.delete()
        user.delete()


class TestChallengeFormRequiredFields(unittest.TestCase):
    def setUp(self):
        self.challenge = ChallengeFactory.attributes()

    def tearDown(self):
        self.challenge = None

    def test_lost_title(self):
        self.challenge['title'] = ''
        self.lost_field()

    def test_wrong_startat(self):
        self.challenge['start_at'] = ''
        self.lost_field()
        self.challenge['start_at'] = 'as 33'
        self.lost_field()

    def test_lost_summary(self):
        self.challenge['summary'] = ''
        self.lost_field()

    def test_wrong_cause(self):
        self.challenge['cause'] = -1
        self.lost_field()
        self.challenge['cause'] = 3
        self.lost_field()

    def test_lost_slug(self):
        self.challenge['slug'] = ''
        self.lost_field()
        self.challenge['slug'] = '1#3'
        self.lost_field()

    def lost_field(self):
        form = ChallengeForm(self.challenge)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())


class ActivityFormTest(unittest.TestCase):
    def setUp(self):
        self.challenge = ChallengeFactory()
        self.user = self.challenge.creator
        self.activity = ActivityFactory.attributes()
        self.activity['challenge'] = self.challenge.pk
        self.activity['creator'] = self.user.pk

    def tearDown(self):
        self.activity = None
        self.user.delete()
        self.challenge.delete()

    def test_form(self):
        form = ActivityForm(self.activity)
        self.assertIsNotNone(form)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())


class ActivityFormRequiredFields(unittest.TestCase):

    def setUp(self):
        self.challenge = ChallengeFactory()
        self.user = UserFactory()
        self.activity = ActivityFactory.attributes()
        self.activity['challenge'] = self.challenge.pk
        self.activity['creator'] = self.user.pk

    def tearDown(self):
        self.activity = None
        self.user.delete()
        self.challenge.creator.delete()
        self.challenge.delete()

    def test_correct(self):
        form = ActivityForm(self.activity)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_lost_title(self):
        self.activity['title'] = ''
        form = ActivityForm(self.activity)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_lost_reward(self):
        self.activity['reward'] = ''
        form = ActivityForm(self.activity)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_lost_reward_cost_type(self):
        self.activity['reward_cost_type'] = ''
        form = ActivityForm(self.activity)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

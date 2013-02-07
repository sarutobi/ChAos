# coding: utf-8

import unittest

from challenge.forms import ChallengeForm
from .factories import ChallengeFactory, UserFactory


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

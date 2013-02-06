# coding: utf-8

import unittest
from datetime import datetime

from django.core.exceptions import ValidationError

from .factories import ChallengeFactory


class ChallengeTest(unittest.TestCase):

    def setUp(self):
        self.challenge = ChallengeFactory.build()

    def tearDown(self):
        self.challenge = None

    def test_creation(self):
        self.assertIsNotNone(self.challenge)

    def test_unicode(self):
        self.assertEqual("%s" % self.challenge, self.challenge.title)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.challenge.get_absolute_url(),
            '/challenge/%s' % self.challenge.slug)


class ChallengePeriodTest(unittest.TestCase):

    def setUp(self):
        self.low_date = datetime(2012, 1, 2, 8, 0, 0)
        self.hi_date = datetime(2012, 2, 1, 8, 0, 0)

    def tearDown(self):
        self.low_date = None
        self.hi_date = None

    def test_dates(self):
        self.assertNotEqual(self.low_date, self.hi_date)

    def test_wrong_period(self):
        challenge = ChallengeFactory.build(
            start_at=self.hi_date,
            end_at=self.low_date
        )
        with self.assertRaises(ValidationError):
            challenge.full_clean()
        challenge = None

    def test_zero_period(self):
        challenge = ChallengeFactory.build(
            start_at=self.hi_date,
            end_at=self.hi_date
        )
        with self.assertRaises(ValidationError):
            challenge.full_clean()
        challenge = None


#class ActivityTest(unittest.TestCase):
#
#    def setUp(self):
#        self.activity = ActivityFactory.build()
#
#    def tearDown(self):
#        self.activity = None

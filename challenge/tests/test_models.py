# coding: utf-8

import unittest
from datetime import datetime

from django.core.exceptions import ValidationError

from challenge.models import Activity, validate_cost
from .factories import ChallengeFactory, ActivityFactory, UserFactory


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

    def test_pk(self):
        self.assertIsNone(self.challenge.pk)


class ChallengeSaveTest(unittest.TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.challenge = ChallengeFactory(creator=self.user)

    def tearDown(self):
        self.user.delete()
        self.challenge.delete()

    def test_store(self):
        self.assertIsNotNone(self.challenge)


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


class ActivityTest(unittest.TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.challenge = ChallengeFactory()
        self.activity = ActivityFactory.build(challenge=self.challenge)

    def tearDown(self):
        self.challenge.delete()
        self.user.delete()
        self.activity = None

    def test_creation(self):
        self.assertIsNotNone(self.activity)

    def test_unicode(self):
        self.assertEqual(self.activity.title, "%s" % self.activity)

    def test_get_absolute_url(self):
        self.activity.creator = self.user
        self.activity.save()
        self.assertEqual(
            self.activity.get_absolute_url(),
            '/challenge/activity/%s' % self.activity.pk)
        self.activity.delete()


class ActivityCostTest(unittest.TestCase):

    def test_cost_task_complete(self):
        self.assertTrue(validate_cost(Activity.TASK_COMPLETION))
        with self.assertRaises(ValidationError):
            validate_cost(Activity.TASK_COMPLETION, 10)

    def test_cost_task_hours(self):
        self.assertTrue(validate_cost(Activity.TASK_HOURS, 2))
        with self.assertRaises(ValidationError):
            validate_cost(Activity.TASK_HOURS)

    def test_cost_task_donation(self):
        self.assertTrue(validate_cost(Activity.TASK_DONATION, 2))
        with self.assertRaises(ValidationError):
            validate_cost(Activity.TASK_DONATION)

    def test_cost_task_servie(self):
        self.assertTrue(validate_cost(Activity.TASK_SERVICE, 2))
        with self.assertRaises(ValidationError):
            validate_cost(Activity.TASK_SERVICE)


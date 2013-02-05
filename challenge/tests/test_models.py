# coding: utf-8

import unittest
from datetime import datetime

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
        self.assertEqual(self.challenge.get_absolute_url(),
                         '/challenge/%s' % self.challenge.slug)

    def test_clean(self):
        date1 = datetime.now()
        date2 = datetime.now()
        self.assertNotEqual(date1, date2)
        challenge = ChallengeFactory.build()



#class ActivityTest(unittest.TestCase):
#
#    def setUp(self):
#        self.activity = ActivityFactory.build()
#
#    def tearDown(self):
#        self.activity = None

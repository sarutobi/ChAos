# coding: utf-8

import unittest

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
                        'challenge')

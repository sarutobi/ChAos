# coding: utf-8

import unittest

from django.test.client import Client


class TestChallengeList(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.resp = self.client.get('/challenge/')

    def tearDown(self):
        self.client = None

    def test_challenge_response(self):
        self.assertEqual(200, self.resp.status_code)

    def test_challenge_moved(self):
        self.assertEqual(301, self.client.get('/challenge').status_code)

    def test_challenge_template(self):
        self.assertIn(
            'challenge_list.html',
            [x.name for x in self.resp.templates])

    def test_challenge_context(self):
        self.assertIsNotNone(self.resp.context['challenges'])

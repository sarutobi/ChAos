# coding: utf-8

import unittest

from django.test.client import Client


class TestChallengeList(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        self.client = None

    def test_challenge_response(self):
        resp = self.client.get('/challenge/')
        self.assertEqual(200, resp.status_code)

    def test_challenge_moved(self):
        self.assertEqual(301, self.client.get('/challenge').status_code)

    def test_challenge_template(self):
        resp = self.client.get('/challenge/')
        self.assertIn('challenge_list.html', [x.name for x in resp.templates])

    def test_challenge_context(self):
        resp = self.client.get('/challenge/')
        self.assertIsNotNone(resp.context['challenges'])

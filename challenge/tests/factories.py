# coding: utf-8

import factory
import random
from datetime import datetime

from django.contrib.auth.models import User

from challenge.models import Challenge, Activity


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    first_name = 'Dummy'
    last_name = 'User'
    email = factory.LazyAttribute(
        lambda a: "{0}@example.com".format(a.username).lower())
    username = factory.Sequence(lambda n: 'username_%s' % n)


class ChallengeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Challenge

    title = factory.Sequence(lambda n: "Challenge_%s" % n)
    summary = factory.Sequence(lambda n: "Description for challenge %s" % n)
    description = factory.LazyAttribute(lambda a: a.summary * 6)
    cause = random.randint(0, 2)
    slug = factory.LazyAttribute(lambda a: "%s_slug" % a.title.lower())
    start_at = datetime(2012, 1, 1, 8, 0, 0)
    end_at = datetime(2012, 2, 1, 8, 0, 0)
    creator = factory.SubFactory(UserFactory)


class ActivityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Activity

    title = factory.Sequence(lambda n: "Activity %s" % n)
    description = factory.LazyAttribute(lambda a: a.title * 3)
    reward = random.randint(3, 10)
    reward_cost = random.randint(2, 20)
    reward_cost_type = random.randint(1, 4)
    challenge = factory.SubFactory(ChallengeFactory)
    creator = factory.SubFactory(UserFactory)

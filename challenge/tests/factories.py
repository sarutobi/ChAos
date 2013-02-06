# coding: utf-8

import factory
import random
from datetime import datetime

from challenge.models import Challenge, Activity


class ChallengeFactory(factory.Factory):
    FACTORY_FOR = Challenge

    title = factory.Sequence(lambda n: "Challenge_%s" % n)
    summary = factory.Sequence(lambda n: "Description for challenge %s" % n)
    description = factory.LazyAttribute(lambda a: a.summary * 6)
    cause = random.randint(0, 4)
    slug = factory.LazyAttribute(lambda a: "%s_slug" % a.title.lower())
    start_at = datetime(2012, 1, 1, 8, 0, 0)
    end_at = datetime(2012, 2, 1, 8, 0, 0)


class ActivityFactory(factory.Factory):
    FACTORY_FOR = Activity

    title = factory.Sequence(lambda n: "Activity %s" % n)
    description = factory.LazyAttribute(lambda a: a.title * 3)
    reward = random.randint(3, 10)
    reward_cost = random.randint(2, 20)
    reward_cost_type = random.randint(1, 4)

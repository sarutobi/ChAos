# coding: utf-8

import factory
import random

from challenge.models import Challenge, Activity


class ChallengeFactory(factory.Factory):
    FACTORY_FOR = Challenge

    title = factory.Sequence(lambda n: "Challenge_%s" % n)
    summary = factory.Sequence(lambda n: "Description for challenge %s" % n)
    description = factory.LazyAttribute(lambda a: a.summary * 6)
    cause = random.randint(0, 4)
    slug = factory.LazyAttribute(lambda a: "%s_slug" % a.title.lower())

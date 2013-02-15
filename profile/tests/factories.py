# coding: utf-8

import factory

from django.contrib.auth.models import User


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: "username_%s" % n)
    first_name = "Dummy"
    last_name = "User"
    password = "123"
    email = factory.LazyAttribute(lambda a: "%s@example.com" % a.username)

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop("password", None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
        if create:
            user.save()
        return user

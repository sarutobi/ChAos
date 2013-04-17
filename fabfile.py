# coding: utf-8

import os
from fabric.api import *

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
MANAGE = os.path.join(ROOT_DIR, 'manage.py')


def test():
    local('%s test --settings=ChAos.settings.test' % MANAGE)


def server():
    local('%s runserver --settings=ChAos.settings.dev_sarutobi' % MANAGE)


def coverage():
    local('coverage run %s test --settings=ChAos.settings.test' % MANAGE)

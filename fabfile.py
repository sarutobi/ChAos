# coding: utf-8

import os
from fabric.api import *

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
MANAGE = os.path.join(ROOT_DIR, 'manage.py')


def test():
    local('%s test --settings=ChAos.settings.test' % MANAGE)

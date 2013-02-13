# coding: utf-8
# Add jenkins ci support

from .test import *

INSTALLED_APPS += (
    'django_jenkins',
)

JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                 'django_jenkins.tasks.run_pep8',
                 'django_jenkins.tasks.run_pyflakes',
                 'django_jenkins.tasks.with_coverage',
                 'django_jenkins.tasks.dir_tests',)

#Coverage excludes
COVERAGE_EXCLUDES = (
    'migrations',
    'tests',
)

PROJECT_APPS = (
    'challenge',
    'profile',
)

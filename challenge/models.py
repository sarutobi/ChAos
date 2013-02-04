# -*- coding: utf-8 -*-

from django.utils.translations import ugettext as _
from django.db import models
from django.contrib.auth.models import User


def logo_path(instance, filename):
    return u"logo/%s/%s" % (instance.slug, filename)


class Challenge(models.Model):
    '''
    Challenge is a group of tasks, that should be completed by participants.
    Each challenge have its own active period, activities durinig challenge
    and allowed participatns. The last one can be individual users or user
    groups, for more deatila about participants see participants.
    '''
    # Challenge name
    name = models.CharField(max_length=100, verbose_name=_('name'))
    # Short description
    summary = models.CharField(max_length=255, verbose_name=_('summary'))
    # Challenge description
    description = models.TextField(blank=True, verbose_name=_('description'))

    slug = models.SlugField(verbose_name=_('slug'))
    # Challenge start
    start_at = models.DateTimeField(verbose_name=_('start at'))
    # Challenge finish
    end_at = models.DateTimeField(verbose_name=_('end at'))
    # Challenge logo
    logo = models.FileField(upload_to=logo_path, blank=True, null=True,
                            verbose_name=_('logo'))

    # Internal fields
    # Challenge creation time
    created_at = models.DateTimeField(auto_now_add=True, editable=False,
                                      verbose_name=_('created at'))
    # Challenge creator
    creator = models.ForeignKey(User, editable=False,
                                verbose_name=_('creator'))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            test = Challenge.objects.get(id=self.id)
            if test.logo.path != self.logo.path:
                test.logo.delete(save=False)
        except ValueError:
            pass
        super(Challenge, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.logo.storage, self.logo.path
        super(Challenge, self).delete(*args, **kwargs)
        storage.delete(path)

    def get_absolute_url(self):
        return ('/app/view/%s' % self.slug)


class Activity(models.Model):
    '''
    Simple task description. Each task must be connected to one Challenge.
    '''
    TASK_STATUS = (
        (0, 'Created'),
        (1, 'In progress'),
        (2, 'Pending'),
        (3, 'Valid'),
        (4, 'Invalid'),
        (5, 'Error'),
    )
    challenge = models.ForeignKey(Challenge, verbose_name=_('challenge'))
    title = models.CharField(max_length=100, verbose_name=('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    points = models.PositiveIntegerField(verbose_name=_('points'))
    #Only authorized users can create tasks
    user = models.ForeignKey(User)
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    valid_until = models.DateTimeField(blank=True, null=True)
    status = models.PositiveIntegerField(choices=TASK_STATUS, default=0)
    # Priority - value between 0 (low) and 100 (utmost) - hint for tracker
    priority = models.PositiveIntegerField()
    #Number of answers to complete task
    quorum = models.PositiveIntegerField()
    #Max numbers of task runs
    max_runs = models.PositiveIntegerField(default=20)
    current_runs = models.PositiveIntegerField(default=0, editable=False)

    def __unicode__(self):
        return "#%s" % self.id

    def is_completed(self):
        return self.quorum <= self.current_runs


class TaskRun(models.Model):
    '''
    When user solve a task, store answer and related information here.
    '''
    task = models.ForeignKey(Task)
    application = models.ForeignKey(Application)
    info = JSONField()
    remote_ip = models.IPAddressField()
    user = models.ForeignKey(User, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    accepted = models.BooleanField(default=False)


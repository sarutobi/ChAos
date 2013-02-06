# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def logo_path(instance, filename):
    return u"logo/%s/%s" % (instance.slug, filename)


CAUSE = (
    (0, _("All")),
    (1, _("Health and care")),
    (2, _("elders")),
)


class Challenge(models.Model):
    '''
    Challenge
    =========
    Challenge is a group of tasks, that should be completed by participants.
    Each challenge have its own active period, activities durinig challenge
    and allowed list ofparticipatns. The last one can be individual user
    or user group. For more deatils about participants see participants.
    '''
    # Challenge name
    title = models.CharField(max_length=100, verbose_name=_('title'))
    # Short description
    summary = models.CharField(max_length=255, verbose_name=_('summary'))
    # Challenge description
    description = models.TextField(blank=True, verbose_name=_('description'))

    cause = models.IntegerField(choices=CAUSE)
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
        return self.title

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

    @models.permalink
    def get_absolute_url(self):
        return ('challenge_view', [self.slug, ])

    def clean(self):
        if self.start_at >= self.end_at:
            raise ValidationError(
                _("'Start at' (%s) should be before 'end at'(%s)"
                  % (self.start_at, self.end_at)))


class Activity(models.Model):
    '''
    Activity
    ========
    Each challenge contains one or more activities - a smallest part of user
    action. Activity can be vary - reading books, push-ups, make food, creation
    month report and so on.
    When user completes the activity, he got a reward - predefined
    number of 'points', that can be converted in some useful things.
    For now completion must be one of predefined values:
    * User confirm task
    * User spent <num> work hours for this activity
    * User sent <predefined> amount of money
    * User spent <num> non-working hours for this activity
    Every complete activity item from this list will be rewarded when one of
    challenge moderators confirm user action.
    '''
    REWARD_COST_TYPE = (
        (1, _("Task completion")),
        (2, _("Hours")),
        (3, _("Donation")),
        (4, _("Service"))
    )
    # Challenge for activity
    challenge = models.ForeignKey(Challenge, verbose_name=_('challenge'))
    # Activity name
    title = models.CharField(max_length=100, verbose_name=('title'))
    # Activity description
    description = models.TextField(blank=True, verbose_name=_('description'))
    # This reward will be transfered to user points deposit
    reward = models.PositiveIntegerField(verbose_name=_('points'))
    # Reward cost - user must spend this for getting a reward
    reward_cost = models.PositiveIntegerField(blank=True, null=True)
    # Hardly predefined reward cost type
    reward_cost_type = models.IntegerField(choices=REWARD_COST_TYPE)
    #Only authorized users can create tasks
    creator = models.ForeignKey(User, verbose_name=_('creator'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False,
                                      verbose_name=_("created at"))

    def __unicode__(self):
        return self.title

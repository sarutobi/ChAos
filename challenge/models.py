# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist


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
        except (ObjectDoesNotExist, ValueError):
            pass
        super(Challenge, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.logo:
            storage, path = self.logo.storage, self.logo.path
            super(Challenge, self).delete(*args, **kwargs)
            storage.delete(path)

    @models.permalink
    def get_absolute_url(self):
        return ('challenge_view', [self.slug, ])

    def clean(self):
        if self.start_at is None:
            raise ValidationError(_("You must provide 'start at' parameter!"))
        if self.end_at is None:
            raise ValidationError(_("You must provide 'end at' parameter!"))
        if self.start_at >= self.end_at:
            raise ValidationError(
                _("'Start at' (%s) should be before 'end at'(%s)"
                  % (self.start_at, self.end_at)))

    def add(self, activity):
        '''
        Append activity to  current challenge
        '''
        activity.challenge = self
        activity.save()


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
    # Activities cost type constants
    TASK_COMPLETION = 1
    TASK_HOURS = 2
    TASK_DONATION = 3
    TASK_SERVICE = 4
    # Cost type choices
    REWARD_COST_TYPE = (
        (TASK_COMPLETION, _("Task completion")),
        (TASK_HOURS, _("Hours")),
        (TASK_DONATION, _("Donation")),
        (TASK_SERVICE, _("Service"))
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
    # Next two fields will be set automatically
    creator = models.ForeignKey(User, verbose_name=_('creator'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False,
                                      verbose_name=_("created at"))

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('activity_view', [self.pk, ])


def validate_cost(cost_type=None, cost_reward=None):
    ''' Activity reward cost validator'''
    if cost_type == Activity.TASK_COMPLETION and cost_reward is not None:
        raise ValidationError(_("Task completion can't have parameter!"))
    if cost_reward is None and cost_type in (
        Activity.TASK_HOURS,
        Activity.TASK_DONATION,
            Activity.TASK_SERVICE):
            raise ValidationError(
                _("You must provide numeric reward parameter!")
            )
    return True

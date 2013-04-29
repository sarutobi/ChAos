# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Challenge, Activity
from .forms import ChallengeForm, ActivityForm


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_at', 'end_at', 'created_at', 'creator')
    form = ChallengeForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        obj.save()

admin.site.register(Challenge, ChallengeAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'challenge',
        'creator', 'created_at',
        'reward_cost_type', 'reward_cost', 'reward')
    form = ActivityForm
    list_filter = ('challenge', )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        obj.save()

admin.site.register(Activity, ActivityAdmin)

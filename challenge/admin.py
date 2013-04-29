# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Challenge


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_at', 'end_at', 'created_at', 'creator')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        obj.save()

admin.site.register(Challenge, ChallengeAdmin)

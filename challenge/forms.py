# coding: utf-8

from django import forms

from .models import Challenge


class ChallengeForm(forms.ModelForm):
    ''' Form for handle challenges'''
    class Meta:
        model = Challenge



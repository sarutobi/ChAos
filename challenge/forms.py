# coding: utf-8

from django import forms

from .models import Challenge, Activity


class ChallengeForm(forms.ModelForm):
    ''' Form for handle challenges'''
    class Meta:
        model = Challenge


class ActivityForm(forms.ModelForm):
    '''Form for handle activities'''
    class Meta:
        model = Activity

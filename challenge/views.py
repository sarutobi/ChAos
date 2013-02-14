# -*- coding: utf-8 -*-

import logging

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import Challenge, Activity
from .forms import ChallengeForm

logger = logging.getLogger(__name__)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class ChallengeList(ListView):
    '''Show all acive applications'''
    template_name = "challenge_list.html"
    context_object_name = "challenges"

    def get_queryset(self):
        return Challenge.objects.all()


class ChallengeView(DetailView):
    model = Challenge
    template_name = "challenge_detail.html"
    context_object_name = "challenge"


class ChallengeCreation(CreateView):
    model = Challenge
    form_class = ChallengeForm
    template_name = 'challenge_form.html'


class ChallengeEdit(UpdateView):
    pass


class ActivityView(DetailView):
    model = Activity
    template = "activity_detail.html"
    context_object_name = "activity"

# -*- coding: utf-8 -*-

import logging

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from ChAos.braces.views import LoginRequiredMixin

from .models import Challenge, Activity
from .forms import ChallengeForm, ActivityForm

logger = logging.getLogger(__name__)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def index(request):
    return render_to_response(
        'index.html',
        context_instance=RequestContext(request))


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


class ChallengeCreation(LoginRequiredMixin, CreateView):
    model = Challenge
    form_class = ChallengeForm
    template_name = 'challenge_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(ChallengeCreation, self).form_valid(form)


class ChallengeEdit(UpdateView):
    pass


class ActivityView(DetailView):
    model = Activity
    template = "activity_detail.html"
    context_object_name = "activity"


class CreateActivity(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'challenge_form.html'
    success_url = '/challenge/'

    def get(self, request, *args, **kwargs):
        self.initial['challenge'] = Challenge.objects.get(slug=kwargs['slug'])
        return super(CreateActivity, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreateActivity, self).form_valid(form)


def join_to_challenge(request, slug):
    ''' Joins current user to selected challenge'''
    challenge = Challenge.objects.get(slug=slug)
    challenge.join(request.user)
    return HttpResponseRedirect('/')

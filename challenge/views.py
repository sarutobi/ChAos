# -*- coding: utf-8 -*-

import logging
from random import choice

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect

from .models import Challenge, Activity
from crowdtask.forms import ApplicationForm, TaskForm

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


#class CreateUser(CreateView):
#    '''Register form'''
#    form_class = UserCreationForm
#    template_name = "register_form.html"
#    success_url = "/"


#def create_app(request):
#    '''create app form'''
#    if request.method == 'GET':
#        return TemplateResponse(request, 'application_form.html',
#            {'form': ApplicationForm(), })
#    elif request.method == 'POST':
#        form = ApplicationForm(request.POST)
#        if form.is_valid():
#            app = form.save(commit=False)
#            app.user_id = request.user.id
#            logger.debug("App data: %s" % app)
#            app.save()
#            return HttpResponseRedirect('/')
#        return TemplateResponse(request, 'application_form.html',
#            {'form': form,})

#def create_task(request):
#    ''' create task form'''
#    if request.method == 'GET':
#        return TemplateResponse(request, 'application_form.html',
#            {'form': TaskForm(),})


#class CreateTask(CreateView):
#    '''
#    Task creation functionality.
#    '''
#    form_class = TaskForm
#    template_name = "application_form.html"
#    success_url = "/apps/created"
#    initial = {}
#
#    def get(self, request, *args, **kwargs):
#        self.initial['application'] =  kwargs.get('pk')
#        return super(CreateView, self).get(request, *args, **kwargs)

#    def form_valid(self, form):
#        task = form.save(commit=False)
#        task.user_id = self.request.user.pk
#        task.status = 0
#        task.save()
#        return redirect(self.success_url)


#class AppTasksList(ListView):
#    '''Show tasks, linked to specific application'''
#    template_name = 'task_list.haml'
#    context_object_name = 'tasks'
#
#    def get_context_data(self, **kwargs):
#        context = super(AppTasksList, self).get_context_data(**kwargs)
#        context['app'] = self.app
#        return context
#
#    def get_queryset(self):
#        self.app = Application.objects.get(slug=self.kwargs.get('slug'))
#        return Task.objects.filter(application=self.app)
#
#
#class UpdateApp(UpdateView):
#    ''' Update application data view'''
#    model = Application
#    form_class = ApplicationForm
#    template_name = "application_form.html"
#    success_url = "/apps/created"
#
#
#class AppDetails(DetailView):
#    '''Application details view'''
#    model = Application
#    template_name = "application_details.html"
#    context_object_name = "app"
#
#
#class UserProfile(DetailView):
#    '''Own user profile view'''
#    model = User
#    template_name="user_profile.html"
#
#    def get_object(self):
#        return self.request.user
#
#
#class UserApps(ListView):
#    '''Self created applications'''
#    template_name="user_applications.html"
#    context_object_name = 'apps'
#
#    def get_queryset(self):
#        return Application.objects.filter(user_id=self.request.user.id)
#
#
#class BaseTaskView(DetailView):
#    '''Show task for user and get an answer'''
#    template_name = "task_skeleton.html"
#
#    def get_object(self):
#        task = TaskRun.objects.exclude(user=self.request.user)
#        task_id = Task.objects.exclude(id__in=task).values('id')
#        return Task.objects.select_related('application').get(id=choice(task_id)['id'])

# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.views.generic.edit import FormView

from .forms import SignUpForm


class CreateUser(FormView):
    template_name = 'registration_form.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

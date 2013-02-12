# coding: utf-8

from django import forms
from django.db.models.signals import post_save
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from profile.models import Profile


class SignUpForm(UserCreationForm):
    """ Require email address when a user signs up """
    email = forms.EmailField(label=_('email address'), max_length=75)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError(
                _("This email address already exists. \
                  Did you forget your password?"))
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = False  # change to false if using email activation
        if commit:
            user.save()
        return user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

# coding: utf-8

from django.conf.urls import patterns, include, url

from .views import ChallengeList, ChallengeView

urlpatterns = patterns(
    "",
    url(r'^$', ChallengeList.as_view(), name="challenges_list"),
    url(r'^(?P<slug>.+$)', ChallengeView.as_view(),
        name="challenge_view"),
)

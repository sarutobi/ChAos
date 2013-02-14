# coding: utf-8

from django.conf.urls import patterns, include, url

from .views import (
    ChallengeList, ChallengeView, ChallengeCreation, ChallengeEdit,
    ActivityView
)

urlpatterns = patterns(
    "",
    url(r'^$', ChallengeList.as_view(), name="challenges_list"),
    url(r'^create$', ChallengeCreation.as_view(), name='challenge_create'),
    url(r'^view/(?P<slug>[\w_-]+$)', ChallengeView.as_view(),
        name="challenge_view"),
    url(r'^activity/(?P<id>\d+$)', ActivityView.as_view(),
        name="activity_view"),
)

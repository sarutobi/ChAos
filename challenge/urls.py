# coding: utf-8

from django.conf.urls import patterns, include, url

from .views import (
    ChallengeList, ChallengeView, ChallengeCreation, ChallengeEdit,
    ActivityView, CreateActivity
)

urlpatterns = patterns(
    "",
    url(r'^$', ChallengeList.as_view(), name="challenges_list"),
    url(r'^create$', ChallengeCreation.as_view(), name='challenge_create'),
    url(r'^view/(?P<slug>[\w_-]+$)', ChallengeView.as_view(),
        name="challenge_view"),
    url(r'^join/(?P<slug>[\w_-]+$)', 'challenge.views.join_to_challenge',
        name='join_to_challenge'),
    url(r'^activity/(?P<id>\d+$)', ActivityView.as_view(),
        name="activity_view"),
    url(r'^appendactivity/(?P<slug>[\w_-]+$)', CreateActivity.as_view(),
        name='appendactivity_view'),
)

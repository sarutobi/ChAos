# coding: utf-8

from django.conf.urls import patterns, include, url

from .views import ChallengeList

urlpatterns = patterns(
    "",
    url(r'^challenge$', ChallengeList.as_view(), name="challenges_list")
)

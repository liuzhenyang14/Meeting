# -*- coding: utf-8 -*-
#
from django.conf.urls import url


from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^user/joinConf/?$', JoinConf.as_view()),
    url(r'^meeting/detail/?$', MeetingDetail.as_view()),
]

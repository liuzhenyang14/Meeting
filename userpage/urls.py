# -*- coding: utf-8 -*-
#
from django.conf.urls import url


from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [

    url(r'^meeting/paysucess?$', JoinConf.as_view()),
    url(r'^meeting/outmeeting?$', CancelConf.as_view()),

    url(r'^meeting?$', MeetingDetail.as_view()),
    url(r'^meeting/pay?$', payDetail.as_view()),
]

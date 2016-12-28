# -*- coding: utf-8 -*-
#
from django.conf.urls import url


from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^meeting/detail/paysucess?$', JoinConf.as_view()),
    url(r'^meeting/detail/outmeeting?$', CancelConf.as_view()),
    url(r'^meeting/detail/?$', MeetingDetail.as_view()),
    url(r'^meeting/detail/pay?$', payDetail.as_view()),
]

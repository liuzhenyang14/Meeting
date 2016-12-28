# -*- coding: utf-8 -*-
#
from django.conf.urls import url
import userpage.views



__author__ = "Epsirom"


urlpatterns = [
    url(r'^user/joinConf/?$', JoinConf.as_view()),
]

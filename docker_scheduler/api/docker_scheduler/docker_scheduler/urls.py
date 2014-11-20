#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

from rest_framework import routers

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()

from controller.v1 import urls


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    url(r'^v1/', include(urls)),
)

# from rest_framework.urlpatterns import format_suffix_patterns
# urlpatterns = format_suffix_patterns(urlpatterns)

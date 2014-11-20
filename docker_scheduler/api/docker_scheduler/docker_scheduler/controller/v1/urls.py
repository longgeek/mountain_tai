#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

from docker_scheduler.controller.v1 import urls_hosts
from docker_scheduler.controller.v1 import urls_images
from docker_scheduler.controller.v1 import urls_flavors
from docker_scheduler.controller.v1 import urls_containers

urlpatterns = patterns(
    '',
    url(r'^hosts/', include(urls_hosts)),
    url(r'^images/', include(urls_images)),
    url(r'^flavors/', include(urls_flavors)),
    url(r'^containers/', include(urls_containers)),
)

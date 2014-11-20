#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

import urls_hosts
import urls_images
import urls_flavors
import urls_containers

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^hosts/', include(urls_hosts)),
    url(r'^images/', include(urls_images)),
    url(r'^flavors/', include(urls_flavors)),
    url(r'^containers/', include(urls_containers)),
)

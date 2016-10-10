#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from usuario import views
from usuario.views import *
import usuario.views as views
#from django.contrib.auth.decorators import login_required



urlpatterns = [
	url(r'^$', views.Login, name='login'),
	url(r'^index/$', views.Index, name='index'),
	url(r'^logout$', views.Logout, name='logout'),
]
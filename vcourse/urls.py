#!eccoding:utf-8

from django.conf.urls import url
from vcourse.views import *

urlpatterns = [
    url(r'^createsection/$', create_section, name='create_section'),
    url(r'^createcourse/$', create_course, name='create_course'),
    url(r'^createpath/$', create_path, name='create_path'),
    url(r'^updatesection/$', update_section, name='update_section'),
    url(r'^updatecourse/$', update_course, name='update_course'),
    url(r'^updatepath/$', update_path, name='update_path'),
    url(r'^deletecourse', delete_course, name='delete_course'),
    url(r'^deletesection/$', delete_section),
    url(r'^deletepath/$', delete_path),
    url(r'^test', vcourse_test),
    url(r'^path', detail_path, name='detail_path'),
    url(r'^section', detail_section, name='detail_section'),
]
#!eccoding:utf-8

from django.conf.urls import url
from vcourse.views import *

urlpatterns = [
    url(r'^create_section/$', create_section, name='create_section'),
    url(r'^create_course/$', create_course, name='create_course'),
    url(r'^create_path/', create_path, name='create_path'),
    url(r'^update_section', update_section, name='update_section'),
    url(r'^update_course', update_course, name='update_course'),
    url(r'^update_path', update_path, name='update_path'),
    url(r'^delete_course', delete_course, name='delete_course'),
    url(r'^test', vcourse_test),
    url(r'^path', detail_path, name='detail_path'),
    url(r'^section', detail_section, name='detail_section'),
]
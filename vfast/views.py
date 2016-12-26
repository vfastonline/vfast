#!encoding:utf-8
import time
import datetime
from django.shortcuts import render
from django.http import HttpResponse
import logging, traceback, json
from vuser import models
from api import encry_password
from django.core.mail import send_mail

#create views in here
def index(request):
    response = HttpResponse('index')
    response.set_cookie('du', datetime.datetime.now(), domain='www.vfast.com')
    response.set_cookie('duminchao', datetime.datetime.now(), domain='www.vfast.com/me',)
    name = 'hello'
    value = 'world'
    response.set_cookie(name, value=value, max_age=3333333)
    return response


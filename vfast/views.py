#!encoding:utf-8
import time
import datetime
from django.shortcuts import render
from django.http import HttpResponse
import logging, traceback, json
from vuser import models
from api import encry_password

#create views in here
def index(request):
    response = render(request, 'index.html', {'role': request.session.get('email', '未登录')})
    # response.set_cookie('du', datetime.datetime.now(), domain='www.vfast.com')
    # response.set_cookie('duminchao', datetime.datetime.now(), domain='www.vfast.com/me',)
    # name = 'hello'
    # value = 'world'
    # # del request.session['role']
    # response.set_cookie(name, value=value, max_age=3333333)
    return response

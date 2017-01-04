#!encoding:utf-8
import models
from django.shortcuts import redirect
from django.http import HttpResponse
import logging, traceback, json
from vfast.api import validate, get_validate
from django.conf import settings
from django import forms


def auth_login(func):
    """登陆装饰器"""
    def wrapper(request, *args, **kwargs):
        try:
            # token = request.session.get('token', None)
            token = request.META.get('HTTP_TOKEN', None)
            print token
            if token is None:
                return HttpResponse(json.dumps({'code':1, 'msg': '您还未登录,请先登录!'}, ensure_ascii=False))
            res = validate(token, settings.SECRET_KEY)
            res = json.loads(res)
            print res
            if res['code'] ==0:
                return func(request, *args, **kwargs)
            else:
                return redirect('/vuser/login/')
        except:
            logging.getLogger().error(traceback.format_exc())
            return redirect('/vuser/login/')
    return wrapper


def require_role(role=0):
    """判断用户角色装饰器"""
    def _deco(func):
        def __deco(request, *args, **kwargs):
            # request.session['pre_url'] = request.path
            token = request.session.get('token', None)
            if token is None:
                return HttpResponse(json.dumps({'code':1, 'msg': u'您还未登录~!'}, ensure_ascii=False))
            res = validate(token, settings.SECRET_KEY)
            res = json.loads(res)
            # print res, token
            if role != res['role']:
                return HttpResponse(json.dumps({'code':2, 'msg': u'您不是管理员,权限不够~!'}, ensure_ascii=False))
            return func(request, *args, **kwargs)
        return __deco
    return _deco


class HeadimgForm(forms.Form):
    id = forms.IntegerField()
    headimg = forms.FileField()


class ResumeForm(forms.Form):
    id = forms.IntegerField()
    resume = forms.FileField()


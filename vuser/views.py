#!encoding: utf-8
from django.shortcuts import render, redirect
from vfast.api import *
from django.http import HttpResponse
import models
import traceback, time, json
from django.conf import settings
from userapi import auth_login, require_role
from django.db.models import F


# Create your views here.
def user_login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email', None)
            pwd = request.POST.get('password', None)
            password = encry_password(pwd)
            user = models.User.objects.get(email=email)
            if user.status == 1:
                return HttpResponse(json.dumps({'code':3, 'msg': '账号未激活'}, ensure_ascii=False))
            elif user.password != password:
                return HttpResponse(json.dumps({'code':2, 'msg': '密码错误'}, ensure_ascii=False))
            else:
                request.session['role'] = user.role
                request.session['email'] = user.email
                print user.role, request.session.get('role')
                token = get_validate(user.email, user.id, user.role, settings.SECRET_KEY)
                request.session['token'] = token
                return HttpResponse(json.dumps({'code':0, 'msg': '登陆成功'}, ensure_ascii=False))
        else:
            return render(request, 'login.html')
    except:
       logging.getLogger().error('%s' % traceback.format_exc())
       return HttpResponse(json.dumps({'code':1 , 'msg': '账号不存在'}, ensure_ascii=False))


@auth_login
def user_logout(request):
    if 'role' not in request.session:
        return redirect('/')
    else:
        del request.session['role']
        del request.session['email']
    return  redirect('/')


def user_register(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email', None)
            pwd = request.POST.get('password', None)
            pwdrpt = request.POST.get('pwdrpt', None)
            # print email, pwd, pwdrpt
            if pwd != pwdrpt:
                return HttpResponse(json.dumps({'code':3, 'msg':'密码不一致'}, ensure_ascii=False))
            user = models.User.objects.filter(email=email)
            print user
            if len(user) == 1:
                return HttpResponse(json.dumps({'code':1 ,'msg': '用户已存在'}, ensure_ascii=False))
            else:
                password = encry_password(pwd)
                regtime = int(time.time())
                uid = encry_password(email, salt=pwd)
                token = encry_password(pwd, salt=email)
                subject = u'Vfast用户账号激活'
                message = u'''
                    恭喜您,注册V-fast学习账号成功!
                    您的账号为: %s
                    V-fast账号需要激活才能正常使用!
                    点我激活账号

                    如果无法点击请复制一下链接到浏览器地址
                    %s/vuser/active?token=%s
                '''  % (email, settings.HOST, token)
                #send_mail('subject',  'message', 'from_email', 'recipient_list', fail_silently=False ) 当fail_silently=False,邮件发送失败,抛出异常
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email,])
                models.User.objects.create(email=email, password=password, regtime=regtime, token=token, uuid=uid)
                return HttpResponse(json.dumps({'code':0 , 'msg': '注册用户成功'}, ensure_ascii=False))
        else:
            return render(request, 'register.html')
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps({'code':2, 'msg': '用户注册失败'}, ensure_ascii=False))


def user_active(request):
    try:
        if request.method == 'GET':
            token = request.GET.get('token', None)
            if token:
                user = models.User.objects.get(token=token)
                if user:
                    models.User.objects.filter(token=token).update(status=0)
                    return HttpResponse(json.dumps({'code':0, 'msg':u'激活成功'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code':2, 'msg': '非法的URL'}))
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps({'code':1, 'msg': '用户激活失败'}, ensure_ascii=False))


def user_resetpwd(request):
    try:
        if request.method == 'GET':
            return render(request, 'vuser/resetpwd.html')
        else:
            email = request.POST.get('email', None)
            user = models.User.objects.get(email=email)
            if user:
                subject = u'[V-fast]找回您的密码'
                message = u'''
                    尊敬的V-fast用户, 您好!
                    您在访问V-fast时点击了"忘记密码"链接, 这是一封密码重置确认邮件。
                    您可以点击以下链接重置账号密码:
                    %s/vuser/resetpassword?uuid=%s
                ''' % (settings.HOST, user.uuid)
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email,])
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'请查看邮件,重置密码'}, ensure_ascii=False))
                except:
                    return HttpResponse(json.dumps({'code': 1, 'msg': u'重置密码失败'}, ensure_ascii=False))
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps({'code':2, 'msg': u'用户不存在'}, ensure_ascii=False))


def user_resetpwd_verify(request):
    try:
        if request.method == 'GET':
            uuid = request.GET.get('uuid', None)
            user = models.User.objects.get(uuid=uuid)
            if user:
                return render(request, 'vuser/resetpwdverify.html', {'user': user})
        else:
            email = request.POST.get('email', None)
            print email
            if email is None:
                return HttpResponse(json.dumps({'code':2, 'msg': u'传递参数错误,需要email'}, ensure_ascii=False))
            password = request.POST.get('password', None)
            password = encry_password(password)
            models.User.objects.filter(email=email).update(password=password)
            return HttpResponse(json.dumps({'code':0, 'msg': u'重置密码成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1, 'msg': u'重置密码失败'}))


@require_role(role=0)
def get_user_list(request):
    try:
        print 'get_user_list'
        users = []
        userall = models.User.objects.all().values('id', 'email', 'username', 'regtime', 'status', 'sumtime',
            'sumscore', 'address', 'birthday', 'company', 'companylocal', 'exceptjob', 'exceptlevel', 'fullname', 'headimg',
            'homepage', 'linkin', 'resume', 'stackoverflow', 'github')
        for user in userall:
            users.append(user)
        return HttpResponse(json.dumps({'code':0, 'users':users}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1}, ensure_ascii=False))

@auth_login
def get_user_detail(request):
    try:
        userid = request.GET.get('id', None)
        if userid:
            userinfo = models.User.objects.filter(id=userid).values('id', 'email', 'username', 'regtime', 'status', 'sumtime',
            'sumscore', 'address', 'birthday', 'company', 'companylocal', 'exceptjob', 'exceptlevel', 'fullname', 'headimg',
            'homepage', 'linkin', 'resume', 'stackoverflow', 'github')[0]
        return HttpResponse(json.dumps({'code':0, 'user': userinfo}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1}, ensure_ascii=False))


@auth_login
def update_user(request):
    try:
        if request.method == 'POST':
            userid = request.POST.get('id', None)
            username = request.POST.get('username', None)
            if userid:
                models.User.objects.filter(id=userid).update(username=username)
                return HttpResponse(json.dumps({'code':0, 'msg': u'用户更新成功'}))
        else:
            return HttpResponse(json.dumps({'code':1, 'msg': u'请求方法错误'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1, 'msg': u'用户更新失败'}, ensure_ascii=False))


@require_role(role=0)
def delete_user(request):
    try:
        if request.method == "POST":
            userid = request.POST.get('id', None)
        elif request.method == 'GET':
            userid = request.GET.get('id', None)
        else:
            return HttpResponse(json.dumps({'code':1, 'msg': u'参数传递错误,需要传递用户id'}))
        models.User.objects.filter(id=userid).delete()
        return HttpResponse(json.dumps({'code': 0, 'msg': u'删除用户成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'数据库操作异常'}, ensure_ascii=False))


def user_course(request):
    """跟踪用户学习路径, 记录用户观看了那些视频, 处理逻辑在vuser_usercourse添加一条记录, 修改用户总得分,观看总时间"""
    try:
        if request.method == 'POST':
            userid = request.POST.get('userid', None)
            courseid = request.POST.get('courseid', None)
            sectionid = request.POST.get('sectionid', None)
            status = request.POST.get('status', None)
            coursetime = request.POST.get('coursetime', None)
            print userid, courseid, sectionid, status, coursetime
            if userid and courseid and sectionid and status and coursetime:
                userid_id = models.User.objects.get(id=userid).id
                courseid_id = models.Course.objects.get(id=courseid).id
                sectionid_id = models.Section.objects.get(id=sectionid).id
                models.UserCourse.objects.create(status=status, userid_id=userid_id, courseid_id=courseid_id,
                                             sectionid_id=sectionid_id)
                models.User.objects.filter(id=userid).update(sumtime=F('sumtime')+coursetime, sumscore=F('sumscore')+1)
                return HttpResponse(json.dumps({'code': 0, 'msg': '记录用户该看视频与否成功'}, ensure_ascii=False))
            else:
                return HttpResponse(
                json.dumps({'code': 1, 'msg': u'参数传递错误, userid, courseid, sectionid, status, coursetime'},
                           ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code':3, 'msg': u'请使用POST请求'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':2, 'msg': '数据库操作异常'}, ensure_ascii=False))


def user_headimg(request):
    try:
        pass
    except:
        pass


def user_resume(request):
    pass

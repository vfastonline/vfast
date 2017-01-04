#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import traceback, json, time
import logging, logging.handlers
import models
from vuser.userapi import require_role
from vfast.api import write_log

# Create your views here.
# @require_role(role=0)
def create_section(request):
    """添加课程视图"""
    try:
        if request.method == 'POST':
            print 'begin'
            email = request.session.get('email')
            tag = request.POST.get('tag', None)
            description = request.POST.get('description', None)
            sectiontype = request.POST.get('sectiontype', None)
            name = request.POST.get('name', None)
            sid = models.SectionType.objects.get(id=sectiontype).id    # 获取需要插入的外键
            sql = models.Section(tag=tag, sumtime=' ', description=description, stypeid_id=sid, name=name)        #外键的插入
            sql.save()
            write_log(email, '创建系列课程%s' % name)
            return HttpResponse(json.dumps({'code':0, 'msg': u'创建系列课程成功'}, ensure_ascii=False))
        else:
            return render(request, 'vcourse/create_section.html')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1, 'msg': '创建系列课程失败'}, ensure_ascii=False))


def update_section(request):
    """编辑课程视图"""
    try:
        if request.method == "GET":
            id = request.GET.get('id', None)
            if id:
                section = models.Section.objects.filter(id=id).values('id', 'tag','sumtime','description', 'stypeid',
                                                                  'stypeid_id', 'name', 'difficulty', 'pubstype')[0]
                return HttpResponse(json.dumps({'code':0, 'section': section}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code':1, 'msg': u'参数传递错误,需要传递sectionid'}, ensure_ascii=False))
        elif request.method == 'POST':
            email = request.session.get('email')
            id = request.POST.get('id', None)
            tag = request.POST.get('tag', None)
            sumtime = request.POST.get('sumtime', None)
            description = request.POST.get('description', None)
            stypeid = request.POST.get('sectiontype', None)
            pubstype = request.POST.get('pubstype', None)
            name = request.POST.get('name', None)
            difficulty = request.POST.get('difficulty', None)
            print stypeid, id, tag, stypeid, pubstype, name, difficulty
            if not (id and stypeid and tag):
                return HttpResponse(json.dumps({'code':1, 'msg': u'输入参数错误'}, ensure_ascii=False))
            else:
                stypeid = models.SectionType.objects.get(id=stypeid)
                result = models.Section.objects.filter(id=id).update(tag=tag, sumtime=sumtime, description=description,
                            stypeid=stypeid, pubstype=pubstype, name=name, difficulty=difficulty) #外键的修改需要传递一个实例对象
                if result:
                    write_log(email, '修改体系课程%s成功~!' % name)
                    return HttpResponse(json.dumps({'code':0, 'msg': u'更新成功'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code':1, 'msg': u'更新失败'}, ensure_ascii=False))
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps({'code':2, 'msg': u'服务器错误'}, ensure_ascii=False))


@require_role(role=0)
def delete_section(request):
    try:
        email = request.session.get('email')
        if request.method == 'POST':
            sectionid = request.POST.get('id', None)
        elif request.method == 'GET':
            sectionid = request.GET.get('id', None)
        else:
            return HttpResponse(json.dumps({'code':1, 'msg': u'非法请求'}, ensure_ascii=False))
        sectionname = models.Section.objects.get(id=sectionid).name
        result = models.Section.objects.filter(id=sectionid).delete()
        if result:
            write_log(email, '删除系列课程成功  课程名为%s' % sectionname)
            return HttpResponse(json.dumps({'code':0, 'msg': u'删除成功'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code':2, 'msg': u'删除失败'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':3, 'msg': u'服务器错误'}, ensure_ascii=False))


#创建课时没写完
def create_course(request):
    try:
        if request.method == "GET":
            return render(request, 'vcourse/create_course.html')
        else:
            print request.FILES
            # cf = CourseForm(request.POST, request.FILES)
            cf = {}
            # if cf.is_valid():
                # sobj = models.Section.objects.get(id=sectionid)
                # sql = models.Course(coursename=coursename, description=desciription, courseware=courseware, videolocal=videolocal, sectionid=sobj, lengtime='41.12', uptime='2011-09-09')
                # sql.save()
            return HttpResponse('successfull')
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps(err_msg, ensure_ascii=False))


def update_course(request):
    try:
        if request.method == "GET":
            id = request.GET.get('id', None)
            course = models.Course.objects.filter(id=id).values('id', 'coursename', 'courseware', 'lengtime', 'description',
                                                                'sectionid', 'videolocal', 'uptime')[0]
            course['lengtime'] = str(course['lengtime'])
            print course
            return HttpResponse(json.dumps({'code':0, 'course':course}, ensure_ascii=False))
        else:
            email = request.session.get('email')
            id = request.POST.get('id', None)
            coursename = request.POST.get('coursename', None)
            description = request.POST.get('description', None)
            sectionid = request.POST.get('sectionid', None)
            sectionid = models.Section.objects.get(id=sectionid).id
            lengtime = request.POST.get('lengtime', None)
            # videolocal = request.POST.get('videllocal', None)
            # uptime = request.POST.get('uptime', None)
            print coursename, description, sectionid, request.POST.get('id')
            result = models.Course.objects.filter(id=id).update(coursename=coursename, description=description, sectionid_id=sectionid,
                                                                lengtime=lengtime)
            if result:
                write_log(email, '修改课时成功, 课时名称为%s' % coursename)
                return HttpResponse(json.dumps({'code':0, 'msg': u'课时修改成功'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code':1, 'msg': u'课时修改错误'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':2, 'msg': u'服务器错误'}, ensure_ascii=False))


def delete_course(request):
    try:
        email = request.session.get('email')
        if request.method == 'GET':
            id = request.GET.get('id', None)
        elif request.method == 'POST':
            id = request.POST.get('id', None)
        else:
            return HttpResponse(json.dumps({'code':2, 'msg': u'非法请求'}, ensure_ascii=False))
        coursename = models.Course.objects.get(id=id).coursename
        result = models.Course.objects.get(id=id).delete()
        if result:
            write_log(email, '删除课时成功, 课时名称为%s' % coursename)
            return HttpResponse(json.dumps({'code':0, 'msg': u'删除课时成功'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code':1, 'msg': u'数据库错误'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':3, 'msg': u'服务器异常'}, ensure_ascii=False))


def create_path(request):
    try:
        if request.method == 'POST':
            email = request.session.get('email')
            name = request.POST.get('name', None)
            description = request.POST.get('description', None)
            sections = request.POST.getlist('sections', [])
            createtime = int(time.time())
            sumtime = request.POST.get('sumtime', None)
            print name, description, sections
            sql = models.Path(name=name, description=description, cretetime=createtime, sumtime=sumtime)
            sql.save()
            for sec in sections:
                secobj = models.Section.objects.get(id=sec)
                sql.sections.add(secobj)
            write_log(email, '创建路径成功, 路径名%s' % name)
            return HttpResponse(json.dumps({'code':0, 'msg': u'创建路径%s成功' % name}))
        else:
            return  render(request, 'vcourse/create_path.html')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1, 'msg': u'创建路径错误'}, ensure_ascii=False))


#这里没写完
def update_path(request):
    try:
        if request.method == 'GET':
            id = request.GET.get('id', None)
            if id:
                return HttpResponse(json.dumps({'code':1, 'msg': u'参数错误,请传pathid'}))
            path = models.Path.objects.filter(id=id).values('id', 'name', 'description', 'sumtime')[0]
            print path
            return HttpResponse(json.dumps({'code':0, 'path': path}))
        else:
            id = request.POST.get('id', None)
            description = request.POST.get('description', None)
            sections = request.POST.getlist('sections', None)
            print id, description, sections
            return HttpResponse('post data')
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps({'code':1, 'msg': u'服务器错误'}, ensure_ascii=False))



def delete_path(request):
    pass



def all_list_course(request):
    courses = models.Course.objects.all().order_by('id')
    return render(request, 'vcourse/test.html', {'data': courses})


def all_List_path(request):
    path = models.Path.objects.all().order_by('id')


def all_list_section(request):
    sections = models.Section.objects.all().order_by('id')


def all_path_section(request):
    pass


def all_section_path(request):
    try:
        if request.method == 'GET':
            pid = request.GET.get('id')
            path_obj = models.Path.objects.get(id=pid)
            sections = path_obj.sections.all()
            print sections
            return render(request, 'vcourse/test.html', {'data': sections})
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps({}))


from course_api import get_all_object
def vcourse_test(request):
    pathall = models.Path.objects.all()
    print pathall[0].sections

    sections = ''
    courses = ''

    return render(request, 'vcourse/test.html', {'paths': pathall, 'sections': sections, 'courses': courses})

def detail_path(request):
    try:
        if request.method == 'GET':
            id = request.GET.get('id', None)
            path_obj = models.Path.objects.get(id=id)
            sections = path_obj.sections.all().order_by('-id')
            print sections[0].id, sections[0].tag
            return render(request, 'vcourse/detail_path.html', {'sections': sections, 'path': path_obj})
    except:
        pass

def detail_section(request):
    try:
        if request.method == 'GET':
            id = request.GET.get('id', None)
            section_obj = models.Section.objects.get(id=id)
            courses = section_obj.course_set.all()
            courses = models.Course.objects.filter(sectionid=section_obj)
            print courses
            return render(request, 'vcourse/detail_section.html', {'section': section_obj, 'courses': courses})
    except:
        pass
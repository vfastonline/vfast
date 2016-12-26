#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import traceback, json
import logging, logging.handlers
from form import SectionForm, CourseForm, PathForm
from models import SectionType, Section, Course, Path

err_msg = {'code':1, 'msg': u'服务器端出现错误'}

# Create your views here.
def create_section(request):
    """添加课程视图"""
    try:
        if request.method == 'POST':
            print 'begin'
            tag = request.POST.get('tag', None)
            description = request.POST.get('description', None)
            sectiontype = request.POST.get('sectiontype', None)
            sid = SectionType.objects.get(id=sectiontype).id    # 获取需要插入的外键
            sql = Section(tag=tag, sumtime=' ', description=description, stypeid_id=sid)        #外键的插入
            sql.save()
            return HttpResponse('successful')
        else:
            cf = SectionForm()
            return render(request, 'vcourse/create_section.html', {'cf': cf})
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps(err_msg, ensure_ascii=False))


def update_section(request):
    """编辑课程视图"""
    try:
        if request.method == "GET":
            id = request.GET.get('id', None)
            section = Section.objects.filter(id=id).values('id', 'tag','sumtime','description', 'stypeid')
            sf = SectionForm(initial=section[0])    #默认选中这里有个小bug,
            return render(request, 'vcourse/update_section.html', {'sf': sf})
        elif request.method == 'POST':
            id = request.POST.get('id', None)
            tag = request.POST.get('tag', None)
            sumtime = request.POST.get('sumtime', None)
            description = request.POST.get('description', None)
            stypeid = request.POST.get('sectiontype', None)
            print stypeid, id, tag
            if not (id and stypeid and tag):
                return HttpResponse(json.dumps({'code':1, 'msg': '输入错误'}, ensure_ascii=False))
            else:
                stypeid = SectionType.objects.get(id=stypeid)
                result = Section.objects.filter(id=id).update(tag=tag, sumtime=sumtime, description=description,
                                                              stypeid=stypeid) #外键的修改需要传递一个实例对象
                if result:
                    return HttpResponse('OK')
                else:
                    return HttpResponse('error')
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps(err_msg, ensure_ascii=False))


def delete_section(request):
    try:
        pass
        # Course.objects.all().order_by()
    except:
        pass


def create_course(request):
    try:
        if request.method == "GET":
            cf = CourseForm()
            return render(request, 'vcourse/create_course.html', {'cf': cf})
        else:
            print request.FILES
            cf = CourseForm(request.POST, request.FILES)
            if cf.is_valid():
                coursename = cf.cleaned_data['coursename']
                videolocal = cf.cleaned_data['videolocal']
                courseware = cf.cleaned_data['courseware']
                desciription = cf.cleaned_data['description']
                sectionid = cf.cleaned_data['sectionid']
                sobj = Section.objects.get(id=sectionid)
                sql = Course(coursename=coursename, description=desciription, courseware=courseware, videolocal=videolocal, sectionid=sobj, lengtime='41.12', uptime='2011-09-09')
                sql.save()
            return HttpResponse('successfull')
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps(err_msg, ensure_ascii=False))


def update_course(request):
    try:
        if request.method == "GET":
            id = request.GET.get('id', None)
            #需要跟form.py里面的name统一
            course = Course.objects.filter(id=id).values('id', 'uptime', 'courseware', 'description',
                                                         'coursename','videolocal', 'sectionid')
            cf = CourseForm(initial=course[0])
            return render(request, 'vcourse/update_course.html', {'cf': cf})
        else:
            coursename = request.POST.get('coursename', None)
            description = request.POST.get('description', None)
            sectionid = request.POST.get('sectionid', None)
            auto_id = request.POST.get('id', None)
            sectionid = Section.objects.get(id=sectionid).id
            print coursename, description, sectionid, request.POST.get('id')
            result = Course.objects.filter(id=auto_id).update(coursename=coursename, description=description, sectionid_id=sectionid)
            if result:
                return HttpResponse('ok')
            else:
                return HttpResponse('mysql update error~!')
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps(err_msg, ensure_ascii=False))


def delete_course(request):
    try:
        if request.method == 'GET':
            id = request.GET.get('id', None)
            print id
            result = Course.objects.get(id=id).delete()
            if result:
                return HttpResponse('Delete OK')
            else:
                return HttpResponse("Delete Error")
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps(err_msg, ensure_ascii=False))


def create_path(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name', None)
            description = request.POST.get('description', None)
            sections = request.POST.getlist('sections', [])
            print name, description, sections
            sql = Path(name=name, description=description)
            sql.save()
            for sec in sections:
                secobj = Section.objects.get(id=sec)
                sql.sections.add(secobj)
            # obj = Path.objects.get(id=3)
            # print (obj.sections.all())
            return HttpResponse('OK')
        else:
            pf = PathForm()
            return  render(request, 'vcourse/create_path.html', {'pf': pf})
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps(err_msg, ensure_ascii=False))


def update_path(request):
    try:
        if request.method == 'GET':
            id = request.GET.get('id')
            print id
            path = Path.objects.filter(id=id).values('id', 'name', 'description')
            print path
            pf = PathForm(initial=path[0])
            return render(request, 'vcourse/update_path.html', {'pf': pf})
        else:
            id = request.POST.get('id', None)
            description = request.POST.get('description', None)
            sections = request.POST.getlist('sections', None)
            print id, description, sections
            return HttpResponse('post data')
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps(err_msg, ensure_ascii=False))


def delete_path(request):
    pass


def all_list_course(request):
    courses = Course.objects.all().order_by('id')
    return render(request, 'vcourse/test.html', {'data': courses})


def all_List_path(request):
    path = Path.objects.all().order_by('id')


def all_list_section(request):
    sections = Section.objects.all().order_by('id')


def all_path_section(request):
    pass


def all_section_path(request):
    try:
        if request.method == 'GET':
            pid = request.GET.get('id')
            path_obj = Path.objects.get(id=pid)
            sections = path_obj.sections.all()
            print sections
            return render(request, 'vcourse/test.html', {'data': sections})
    except:
        logging.getLogger().error('%s' % traceback.format_exc())
        return HttpResponse(json.dumps({}))


from course_api import get_all_object
def vcourse_test(request):
    pathall = Path.objects.all()
    print pathall[0].sections

    sections = ''
    courses = ''

    return render(request, 'vcourse/test.html', {'paths': pathall, 'sections': sections, 'courses': courses})

def detail_path(request):
    try:
        if request.method == 'GET':
            id = request.GET.get('id', None)
            path_obj = Path.objects.get(id=id)
            sections = path_obj.sections.all().order_by('-id')
            print sections[0].id, sections[0].tag
            return render(request, 'vcourse/detail_path.html', {'sections': sections, 'path': path_obj})
    except:
        pass

def detail_section(request):
    try:
        if request.method == 'GET':
            id = request.GET.get('id', None)
            section_obj = Section.objects.get(id=id)
            courses = section_obj.course_set.all()
            courses = Course.objects.filter(sectionid=section_obj)
            print courses
            return render(request, 'vcourse/detail_section.html', {'section': section_obj, 'courses': courses})
    except:
        pass
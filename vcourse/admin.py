#encoding:utf-8
from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(SectionType)
admin.site.register(Path)
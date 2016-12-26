#!encoding:utf-8
from django import forms
from models import SectionType, Section

class SectionForm(forms.Form):
    stypeids = SectionType.objects.all().values_list('id', 'sectiontype')
    id = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={'class': 'form-control hidden'}))
    tag = forms.CharField(required=True, max_length=32, error_messages={'invalid':'tag'},
                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    description = forms.CharField(required=True, max_length=500,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    sumtime = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sectiontype = forms.IntegerField(widget=forms.Select(attrs={'class': 'select2'}, choices=stypeids))

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        self.fields['sectiontype'].widget.choices = SectionType.objects.all().values_list('id', 'sectiontype')


class CourseForm(forms.Form):
    sectionids = Section.objects.all().values_list('id', 'tag')

    id = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={'class': 'form-control hedden'}))
    coursename = forms.CharField(required=True, max_length=30,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    videolocal = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':
                                                                               'form-control'}))

    courseware = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    sectionid = forms.IntegerField(required=True, widget=forms.Select(attrs={'class': 'select2'}, choices=sectionids))

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['sectionid'].widget.choices = Section.objects.all().values_list('id','tag')


class PathForm(forms.Form):
    section = Section.objects.all().values_list('id', 'tag')

    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    sections = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'class': 'select'}, choices=section))

    def __init__(self, *args, **kwargs):
        super(PathForm, self).__init__(*args, **kwargs)
        self.fields['sections'].widget.choices = Section.objects.values_list('id', 'tag')

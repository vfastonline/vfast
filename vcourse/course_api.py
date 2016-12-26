#!encoding: utf-8
from vcourse import models
from models import Course

def get_all_object(models):
    results = models.objects.all().order_by('id')
    return results

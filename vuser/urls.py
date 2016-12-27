#!encoding:utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^login', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^register', views.user_register, name='register'),
    url(r'^active', views.user_active, name='active'),
    url(r'^resetpwd', views.user_resetpwd, name='resetpwd'),
    url(r'^resetpassword', views.user_resetpwd_verify, name='resetpwd_verify'),
    url(r'getuserall', views.get_user_list, name='getuserall'),
    url(r'getuserinfo', views.get_user_detail, name='getuserinfo'),
    url(r'deleteuser', views.delete_user, name='deleteuser'),
    url(r'updateuser', views.update_user, name='updateuser'),
    url(r'^usercourse', views.user_course, name='usercourse'),
]



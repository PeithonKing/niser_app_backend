from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import *


urlpatterns = [
    path('', index_view, name='home'),

	# Schools Views
    path('s/<abbrev>/', school_view, name='school'),
    path('s/<abbrev>/add/', add_crs, name='add_crs'),

	# Course Views
    path('c/<cd>/', course_view, name='course'),
    path('c/<cd>/add/', add_itr, name='add_itr'),

    path('c/<cd>/<yr>/<sea>/', itr_view, name='itr'),
    path('c/<cd>/<yr>/<sea>/add/', add_item, name='add_item'),
    path('c/<cd>/<yr>/<sea>/comment/', add_comment, name='comment'),

    path('comm_del/<cid>/', delete_comment, name='delete_comment'),

    path('f/<source>/<fname>', file_view, name='file'),

    path('report/c/<cid>/', report_comment, name='report_comment'),
    path('report/i/<iid>/', report_item, name='report_item'),
    path('report/u/<uid>/', report_user, name='report_user'),
    
    path('faq/', faq, name='faq'),
    path('log/', log_view, name='log'),
]

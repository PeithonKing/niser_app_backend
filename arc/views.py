from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.db import models

from authtools.models import User

from .models import School, Course, Itr, Item, SEMS, Count
from .forms import *
from my_user.helper import *

import datetime
from .recom import *


# Create your views here.

from niser_app.local_settings import *

REV_DICT_SEMS = dict([i[::-1] for i in SEMS])

def index_view(request):
    school_list = School.objects.order_by('abbr')
    try:
        cnt = Count.objects.get(cnt_id=1)
    except Count.DoesNotExist:
        cnt = Count(cnt_id=1, rec=0, own=0)
        cnt.save()

    if request.user.is_authenticated:
        auth = 1
        rec = get_recom(request.user.id)  # Get Recommendations
        rec_list = Item.objects.filter(fl__in=rec)
    else:
        auth = 0
        rec_list = []
    return render(request, "arc/index.html", {
        "school_list": school_list,
        "auth": auth,
        "recom": rec_list,
        "count": cnt
        })

def school_view(request, abbrev):
    try:
        s = School.objects.get(abbr__iexact=abbrev)
        courses = Course.objects.filter(school=s, appr=True).order_by('code')
        form = CourseForm()
        return render(request, 'arc/school.html', {'sch': s, 'course_list': courses, 'form': form})
    except School.DoesNotExist:
        raise Http404("School not found")

def course_view(request, cd):
    try:
        form = None
        if request.user is not None:
            form = ItrForm()
        c = Course.objects.get(code=cd)
        itrs = Itr.objects.filter(course__code=cd, appr=True).order_by('year', 'sem')
        return render(request, 'arc/course.html', {'crs': c, 'itr_list': itrs, 'form': form})
    except Course.DoesNotExist:
        raise Http404("Course not found")

def itr_view(request, cd, yr, sea):
    try:
        s = REV_DICT_SEMS[sea.title()]
        i = Itr.objects.get(course__code = cd, year=yr, sem=s)
        items = Item.objects.filter(itr=i)
        comments = Comment.objects.filter(itr=i, vis=True)
        form = None
        form2 = CommentReportForm()
        form3 = ItemReportForm()
        form4 = None
        if request.user is not None:
            form = ItemForm()
            form4 = CommentForm()
        return render(request, 'arc/itr.html', {
            'itr': i,
            'item_list': items,
            'comm_list': comments,
            'form': form,
            'report_form': form2,
            'item_report_form': form3,
            'comment_form': form4
            })
    except Exception as e:
        raise e
    # except Itr.DoesNotExist:
        # raise Http404('No such iteration was found')


# def user_view(request, uid):
#     try:
#         u = User.objects.get(id = uid)
#         u2 = request.user
#         if request.method == 'POST':
#             if u2 is not None and u2.is_authenticated and u == u2:
#                 form = ProfileForm(request.POST, instance=u.profile)
#                 pro = form.save(commit=False)
#                 pro.upd = True
#                 pro.save()
#                 return render(request, 'arc/user.html', {'user_page': u, 'form': form})
#             else:
#                 return HttpResponse('You shouldn\'t be here')
#         if request.user.is_authenticated:
#             if u == u2:
#                 form = ProfileForm()
#                 return render(request, 'arc/user.html', {'user_page': u, 'form': form})
#             form = UserReportForm()
#             return render(request, 'arc/user.html', {'user_page': u, 'report_form': form})
#         return render(request, 'arc/user.html', {'user_page': u})
#     except (User.DoesNotExist, ValueError):
#         # ValueError will occur when someone tries /u/asdf (since asdf cannot be parsed as
#         # an integer)
#         raise Http404('User not found')

def add_comment(request, cd, yr, sea):
    url = reverse('itr', args=[cd, yr, sea])
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user is not None:
                comm =  form.save(commit=False)
                comm.user = request.user
                s = REV_DICT_SEMS[sea.title()]
                i = Itr.objects.get(course__code = cd, year=yr, sem=s)
                comm.itr = i
                comm.save()
                return redirect(url)
                return render(request, 'arc/itr.html', {'crs': c, 'itr': itr, 'success': True})
            else:
                return HttpResponse('User is none')

def delete_comment(request, cid):
    c = Comment.objects.get(id = cid)
    if request.user == c.user:
        c.vis = False
        c.save()
        return HttpResponse('<div class="alert alert-success"> Comment successfully deleted </div>')

def add_item(request, cd, yr, sea):
    i = Itr.objects.get(course__code=cd, year=yr, sem=REV_DICT_SEMS[sea.title()])
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user is not None:
                item = form.save(commit=False)
                item.op = request.user
                item.itr = i
                item.save()
                return render(request, 'arc/add-item.html', {'itr': i, 'item': item, 'success': True})
            else:
                return HttpResponse('User is none')
    else:
        form = ItemForm()
    return render(request, 'arc/add-item.html', {'itr': i, 'form': form})

def add_itr(request, cd):
    c = Course.objects.get(code=cd)
    if request.method == 'POST':
        form = ItrForm(request.POST)
        if form.is_valid():
            if request.user is not None:
                itr =  form.save(commit=False)
                itr.op = request.user
                itr.course = c
                try:
                    i = Itr.objects.get(course=c, sem=itr.sem, year=itr.year)
                    return render(request, 'arc/add-itr.html',
                            {'exists': True, 'crs': c, 'itr': itr})
                except Itr.DoesNotExist:
                    itr.save()
                    return render(request, 'arc/add-itr.html', {'crs': c, 'itr': itr, 'success': True})
            else:
                return HttpResponse('User is none')
    else:
        form = ItrForm()
    return render(request, 'arc/add-itr.html', {'crs': c, 'form': form})

def add_crs(request, abbrev):
    s = School.objects.get(abbr=abbrev)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            if request.user is not None:
                cd = form.cleaned_data['code'].lower()
                try:
                    crs = Course.objects.get(code=cd)
                    return render(request, 'arc/add-crs.html',
                            {'exists': True, 'crs': crs})
                except Course.DoesNotExist:
                    crs = Course()
                    crs.code = form.cleaned_data['code'].lower()
                    crs.name = form.cleaned_data['name']
                    crs.op = request.user.profile
                    crs.school = s
                    crs.save()
                    return render(request, 'arc/add-crs.html', {'crs': crs, 'success': True})
            else:
                return HttpResponse('User is none')
    else:
        form = CourseForm()
    return render(request, 'arc/add-crs.html', {'sch': s, 'form': form})

def file_view(request, source, fname):
    try:
        cnt = Count.objects.get(cnt_id=1)
        if source == 'self':
            cnt.own += 1
        elif source == 'recom':
            cnt.rec += 1
        cnt.save()
        i = Item.objects.get(fl=fname)
        if request.user.is_authenticated:
            update_recom(fname, request.user.id)
        return render(request, 'arc/file.html', {'item': i})
    except Item.DoesNotExist:
        raise Http404("File not found")

def report_comment(request, cid):
    if request.method == 'POST':
        rep_form = CommentReportForm(request.POST)
        if rep_form.is_valid():
            if request.user is not None:
                try:
                    c = Comment.objects.get(id=cid)
                    rep = rep_form.save(commit=False)
                    rep.user = request.user
                    rep.comment = c
                    rep.save()
                    return HttpResponse('<div class="alert alert-success"> Report submitted successfully. Thanks. </div>')
                except Comment.DoesNotExist:
                    raise Http404('Comment Not Found')
            return HttpResponse('User is none')
    return HttpResponse('You shouldn\'t be here.')

def report_item(request, iid):
    if request.method == 'POST':
        rep_form = ItemReportForm(request.POST)
        if rep_form.is_valid():
            if request.user is not None:
                try:
                    i = Item.objects.get(id=iid)
                    rep = rep_form.save(commit=False)
                    rep.user = request.user
                    rep.item = i
                    rep.save()
                    return HttpResponse('<div class="alert alert-success"> Report submitted successfully. Thanks. </div>')
                except Item.DoesNotExist:
                    raise Http404('File Not Found')
            return HttpResponse('User is none')
    return HttpResponse('You shouldn\'t be here.')

def report_user(request, uid):
    if request.method == 'POST':
        rep_form = UserReportForm(request.POST)
        if rep_form.is_valid():
            if request.user is not None:
                try:
                    u = User.objects.get(id=uid)
                    rep = rep_form.save(commit=False)
                    rep.user = request.user
                    rep.target = u
                    rep.save()
                    return HttpResponse('<div class="alert alert-success"> Report submitted successfully. Thanks. </div>')
                except User.DoesNotExist:
                    raise Http404('User Not Found')
            return HttpResponse('User is none')
    return HttpResponse('You shouldn\'t be here.')

def faq(request):
    return render(request, 'arc/faq.html')

def log_view(request):

    recent_uploads = Item.objects.all().order_by('-id')[:20]
    t2 = timezone.now()
    for item in recent_uploads:
        if item.time != None:
            t1 = item.time
            delta = t2 - t1
            item.when = readableDuration(delta.total_seconds())
        else:
            item.when = ''

    recent_comments = Comment.objects.all().order_by('-id')[:20]
    for comment in recent_comments:
        t1 = comment.posted
        t2 = timezone.now()
        delta = t2 - t1
        comment.when = readableDuration(delta.total_seconds())

    top_uploaders = Item.objects.values('op').annotate(models.Count('id')).order_by('-id__count')[:10]
    for i in range(len(top_uploaders)):
        top_uploaders[i]['pos'] = i+1
        top_uploaders[i]['op'] = User.objects.get(id=top_uploaders[i]['op'])

    uploads_this_month = Item.objects.filter(time__month = t2.month, time__year = t2.year)
    top_recent_uploaders = uploads_this_month.values('op').annotate(models.Count('id')).order_by('-id__count')[:3]
    for i in range(len(top_recent_uploaders)):
        top_recent_uploaders[i]['pos'] = i+1
        top_recent_uploaders[i]['op'] = User.objects.get(id=top_recent_uploaders[i]['op'])

    # set it to be None if the query set is empty, so that we can catch it in the template
    # is there a better way to do this?
    #if len(top_recent_uploaders) == 0:
    #    top_recent_uploaders = None

    return render(request, 'arc/log.html', {
        'recent_uploads': recent_uploads,
        'recent_comments': recent_comments,
        'top_uploaders': top_uploaders,
        'top_recent_uploaders': top_recent_uploaders
        })

def error404(request, exception):
    return render(request, 'arc/404.html', {'exp': exception}, status=404)

def error500(request, exception):
    return render(request, 'arc/500.html', {'exp': exception}, status=500)

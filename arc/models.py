from django.db import models
from authtools.models import User
from django.core.mail import mail_admins
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

import json

from my_user.models import School, Course

ITEM_TYPES = [
    ('a', 'Quiz'),
    ('b', 'Mid-Semester Exam'),
    ('c', 'End-Semester Exam'),
    ('d', 'Assignment'),
    ('e', 'Notes'),
    ('f', 'Slides'),
    ('g', 'Textbook'),
]

SEMS = [
    ('FA', 'Fall'),
    ('SP', 'Spring'),
    ('SU', 'Summer'),
    ('WI', 'Winter')
]


class Itr(models.Model):
    def __str__(self):
        return self.course.code.upper() + ', ' + self.sem_name + ' ' + self.year

    @property
    def short_name(self):
        return self.course.code.upper() + ' ' + self.sem_name + ' ' + self.year

    @property
    def sem_name(self):
        return dict(SEMS)[self.sem]

    op = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sem = models.CharField('Semester', max_length=2, choices = SEMS, default='FA')
    year = models.CharField('Year', max_length=4)
    inst = models.CharField('Instructor', max_length=512)
    appr = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.appr == False:
            mail_admins(
                subject = 'New Iteration Needs Approval.',
                message = 'A new iteration {} {} was added for course {} by {}.  It is pending approval.'.format(self.sem, self.year, self.course, self.op))

        super().save(*args, **kwargs)


from . import gen
def gen_file_name(instance, filename):
    ext = filename.split('.')[-1]
    file_name = gen.genURL()
    while Item.objects.filter(fl__contains = file_name).count() > 0:
        file_name = gen.genURL()
    return f"static/arc/files/{file_name}.{ext}"

class Item(models.Model):
    def __str__(self):
        return self.name
    op = models.ForeignKey(User, on_delete=models.CASCADE)
    itr = models.ForeignKey(Itr, on_delete=models.CASCADE)
    fl = models.FileField('File', upload_to=gen_file_name)
    name = models.CharField('Name', max_length=64)
    #typ = models.CharField('Type', max_length=3, choices = ITEM_TYPES, default='a')
    desc = models.TextField('Description', max_length=1000, blank=True)
    appr = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now, null=True)

class SolItem(Item):
    def __str__(self):
        return 's' + self.type
    #item = models.ForeignKey(Item, on_delete=models.CASCADE)
    par = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL, related_name='+')


# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itr = models.ForeignKey(Itr, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, blank=False)
    posted = models.DateTimeField(default=timezone.now)
    vis = models.BooleanField(default=True)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.TextField("Description", max_length=1000, blank=True)
    time = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        mail_admins(
            subject = 'New Report Object.',
            message = 'Someone needs to check it out.')

        super().save(*args, **kwargs)

class CommentReport(Report):

    def __str__(self):
        c = self.comment
        return str(c.user) + ' | '+ str(c.id) + ' | ' + str(c.text)

    TYPE_CHOICES = [
        ("ab", "Abusive"),
        ("ma", "Malicious"),
        ("ot", "Off-Topic"),
        ("sp", "Spam"),
        ("oh", "Other"),
    ]
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    typ = models.CharField('What\'s wrong?', max_length=2, choices=TYPE_CHOICES)

class ItemReport(Report):
    TYPE_CHOICES = [
        ("ma", "Malicious"),
        ("ur", "Unrelated"),
        ("du", "Duplicate"),
        ("sp", "Spam"),
        ("oh", "Other"),
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    typ = models.CharField('What\'s wrong?', max_length=2, choices=TYPE_CHOICES)

class UserReport(Report):
    TYPE_CHOICES = [
        ("ab", "Abusive"),
        ("im", "Imposter"),
        ("oh", "Other"),
    ]
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
    typ = models.CharField('What\'s wrong?', max_length=2, choices=TYPE_CHOICES)

class Recom(models.Model):
    userid = models.CharField(max_length=4)
    fname = models.CharField(max_length=50)
    cnt = models.IntegerField(default=1)

# Model to store seperately the no. of files accessed from recommendations
# and no. of files from self browsing.
class Count(models.Model):
    cnt_id = models.IntegerField(primary_key=True, default=1)
    rec = models.IntegerField(default=0)
    own = models.IntegerField(default=0)

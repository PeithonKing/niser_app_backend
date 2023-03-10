# Generated by Django 4.1.3 on 2022-12-20 11:09

import arc.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Count',
            fields=[
                ('cnt_id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('rec', models.IntegerField(default=0)),
                ('own', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('appr', models.BooleanField(default=False)),
                ('op', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True, max_length=1000, verbose_name='Description')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbr', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=256)),
                ('appr', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Itr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem', models.CharField(choices=[('FA', 'Fall'), ('SP', 'Spring'), ('SU', 'Summer'), ('WI', 'Winter')], default='FA', max_length=2, verbose_name='Semester')),
                ('year', models.CharField(max_length=4, verbose_name='Year')),
                ('inst', models.CharField(max_length=512, verbose_name='Instructor')),
                ('appr', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arc.course')),
                ('op', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fl', models.FileField(upload_to=arc.models.gen_file_name, verbose_name='File')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('desc', models.TextField(blank=True, max_length=1000, verbose_name='Description')),
                ('appr', models.BooleanField(default=False)),
                ('time', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('itr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arc.itr')),
                ('op', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arc.school'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('vis', models.BooleanField(default=True)),
                ('itr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arc.itr')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='arc.report')),
                ('typ', models.CharField(choices=[('ab', 'Abusive'), ('im', 'Imposter'), ('oh', 'Other')], max_length=2, verbose_name="What's wrong?")),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('arc.report',),
        ),
        migrations.CreateModel(
            name='SolItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='arc.item')),
                ('par', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='arc.item')),
            ],
            bases=('arc.item',),
        ),
        migrations.CreateModel(
            name='ItemReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='arc.report')),
                ('typ', models.CharField(choices=[('ma', 'Malicious'), ('ur', 'Unrelated'), ('du', 'Duplicate'), ('sp', 'Spam'), ('oh', 'Other')], max_length=2, verbose_name="What's wrong?")),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arc.item')),
            ],
            bases=('arc.report',),
        ),
        migrations.CreateModel(
            name='CommentReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='arc.report')),
                ('typ', models.CharField(choices=[('ab', 'Abusive'), ('ma', 'Malicious'), ('ot', 'Off-Topic'), ('sp', 'Spam'), ('oh', 'Other')], max_length=2, verbose_name="What's wrong?")),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arc.comment')),
            ],
            bases=('arc.report',),
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-19 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_alter_listing_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='op',
            new_name='seller',
        ),
    ]

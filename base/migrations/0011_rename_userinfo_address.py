# Generated by Django 4.2.16 on 2024-10-23 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_rename_firstname_userinfo_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='userInfo',
            new_name='Address',
        ),
    ]

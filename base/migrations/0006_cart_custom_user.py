# Generated by Django 4.2.16 on 2024-10-23 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_usersignup_user_usersignup_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='custom_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.usersignup'),
        ),
    ]

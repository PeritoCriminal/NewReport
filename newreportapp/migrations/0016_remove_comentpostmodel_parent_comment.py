# Generated by Django 5.1.2 on 2024-11-04 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newreportapp', '0015_alter_customusermodel_access_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentpostmodel',
            name='parent_comment',
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-04 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newreportapp', '0017_alter_customusermodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]

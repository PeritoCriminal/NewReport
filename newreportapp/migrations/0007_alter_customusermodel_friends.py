# Generated by Django 5.1.2 on 2024-10-30 21:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newreportapp', '0006_alter_customusermodel_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='user_friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
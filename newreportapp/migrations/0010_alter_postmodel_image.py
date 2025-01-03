# Generated by Django 5.1.2 on 2024-10-31 12:58

import stdimage.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newreportapp', '0009_remove_customusermodel_confirmation_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='image',
            field=stdimage.models.StdImageField(blank=True, force_min_size=False, null=True, upload_to='posts/images/', variations={'large': (1200, 800, True), 'thumbnail': (300, 200, True)}),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-04 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newreportapp', '0018_customusermodel_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
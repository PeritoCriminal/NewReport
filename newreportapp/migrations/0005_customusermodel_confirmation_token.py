# Generated by Django 5.1.2 on 2024-10-30 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newreportapp', '0004_postmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='confirmation_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
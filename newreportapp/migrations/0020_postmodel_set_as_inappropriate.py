# Generated by Django 5.1.2 on 2024-11-05 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newreportapp', '0019_alter_customusermodel_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='set_as_inappropriate',
            field=models.BooleanField(default=False, verbose_name='Marcado como inapropriado'),
        ),
    ]

# Generated by Django 2.2.2 on 2019-06-21 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djh_app', '0002_ttbprevstep_ttbuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttbprevstep',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='updated'),
        ),
    ]

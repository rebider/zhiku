# Generated by Django 2.0 on 2018-07-23 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
        ('task', '0004_auto_20180723_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='roles',
            field=models.ManyToManyField(blank=True, to='rbac.Role', verbose_name='具有的所有的角色'),
        ),
    ]

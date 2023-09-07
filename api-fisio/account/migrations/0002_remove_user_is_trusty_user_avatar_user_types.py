# Generated by Django 4.2.5 on 2023-09-06 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_trusty',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='types',
            field=models.PositiveSmallIntegerField(choices=[(1, 'pacient'), (2, 'Physiotherapist')], default=1, verbose_name='Type'),
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-06 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_user_is_trusty_user_avatar_user_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='types',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pacient'), (2, 'Physiotherapist')], default=1, verbose_name='Type'),
        ),
    ]
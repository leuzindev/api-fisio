# Generated by Django 4.2.5 on 2023-09-07 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_initial'),
        ('account', '0007_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='plans',
            field=models.ManyToManyField(blank=True, to='plan.plan'),
        ),
    ]

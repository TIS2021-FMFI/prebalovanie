# Generated by Django 3.2.8 on 2022-01-18 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0005_alter_log_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'default_permissions': (), 'permissions': (('bla', 'Bla Bla'),), 'verbose_name': 'Log', 'verbose_name_plural': 'Logy'},
        ),
    ]

# Generated by Django 3.2.8 on 2022-01-18 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'default_permissions': (), 'permissions': (('history', 'Prístup k histórii'), ('user', 'Správa používateľov')), 'verbose_name': 'Účet', 'verbose_name_plural': 'Účty'},
        ),
    ]

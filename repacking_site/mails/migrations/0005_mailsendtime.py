# Generated by Django 3.2.8 on 2022-02-09 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0004_alter_mailsendsetting_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailSendTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='Čas')),
            ],
            options={
                'verbose_name': 'Čas posielania mailov',
                'verbose_name_plural': 'Časy posielania mailov',
                'permissions': (),
                'default_permissions': (),
            },
        ),
    ]

# Generated by Django 3.2.8 on 2022-01-18 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0003_alter_mailsendsetting_mail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailsendsetting',
            options={'default_permissions': (), 'permissions': (), 'verbose_name': 'Mailová adresa', 'verbose_name_plural': 'Mailové adresy'},
        ),
    ]

# Generated by Django 3.2.8 on 2022-01-18 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repacking', '0004_auto_20220118_0851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photos',
            options={'default_permissions': (), 'permissions': (), 'verbose_name': 'Fotka', 'verbose_name_plural': 'Fotky'},
        ),
        migrations.AlterModelOptions(
            name='repackhistory',
            options={'default_permissions': (), 'permissions': (), 'verbose_name': 'Prebaľovanie', 'verbose_name_plural': 'Prebaľovania'},
        ),
        migrations.AlterModelOptions(
            name='repackingstandard',
            options={'default_permissions': (), 'permissions': (), 'verbose_name': 'Štandard', 'verbose_name_plural': 'Štandardy'},
        ),
        migrations.AlterModelOptions(
            name='tools',
            options={'default_permissions': (), 'permissions': (), 'verbose_name': 'OPP', 'verbose_name_plural': 'OPP'},
        ),
    ]
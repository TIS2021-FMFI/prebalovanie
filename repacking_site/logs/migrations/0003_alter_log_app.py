# Generated by Django 3.2.8 on 2022-01-18 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_alter_log_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='app',
            field=models.CharField(choices=[('Prebaľovanie', 'Repacking'), ('Správa používateľov', 'User Managment'), ('Posielanie mailov', 'Mail Reports'), ('logovanie', 'Logging')], max_length=25),
        ),
    ]
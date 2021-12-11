# Generated by Django 3.2.8 on 2021-12-10 17:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/')),
            ],
        ),
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='tools/%Y/%m/')),
            ],
        ),
        migrations.CreateModel(
            name='RepackingStandard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SKU', models.CharField(default='', max_length=50, unique=True)),
                ('COFOR', models.CharField(default='', max_length=50)),
                ('supplier', models.CharField(default='', max_length=50)),
                ('destination', models.CharField(default='', max_length=50)),
                ('items_per_move', models.IntegerField(default=0)),
                ('unit_weight', models.DecimalField(decimal_places=4, default=0, max_digits=6)),
                ('repacking_duration', models.DurationField(default=datetime.timedelta(0))),
                ('instructions', models.CharField(default='', max_length=1200)),
                ('input_count_of_items_in_package', models.IntegerField(default=0)),
                ('output_count_of_items_in_package', models.IntegerField(default=0)),
                ('input_count_of_boxes_on_pallet', models.IntegerField(default=0)),
                ('output_count_of_boxes_on_pallet', models.IntegerField(default=0)),
                ('input_count_of_items_on_pallet', models.IntegerField(default=0)),
                ('output_count_of_items_on_pallet', models.IntegerField(default=0)),
                ('input_type_of_package', models.CharField(default='', max_length=50)),
                ('output_type_of_package', models.CharField(default='', max_length=50)),
                ('created', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('input_photos', models.ManyToManyField(blank=True, related_name='input_photos', to='repacking.Photos')),
                ('output_photos', models.ManyToManyField(blank=True, related_name='output_photos', to='repacking.Photos')),
                ('tools', models.ManyToManyField(blank=True, related_name='tools', to='repacking.Tools')),
            ],
        ),
        migrations.CreateModel(
            name='RepackHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repack_start', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('repack_finish', models.DateTimeField()),
                ('repack_duration', models.DurationField(default=datetime.timedelta(0))),
                ('idp', models.CharField(max_length=50)),
                ('repacking_standard', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repacking_standard', to='repacking.repackingstandard')),
                ('users', models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

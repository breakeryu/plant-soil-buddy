# Generated by Django 2.1.4 on 2019-02-08 02:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0009_auto_20190126_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('moist', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ph', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fertility', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='SoilProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=256)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='sensorrecord',
            name='soil_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SoilProfile'),
        ),
    ]

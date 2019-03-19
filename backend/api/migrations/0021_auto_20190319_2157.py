# Generated by Django 2.1.7 on 2019-03-19 14:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20190318_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantLifeCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_name', models.CharField(default='', max_length=100)),
                ('life_cycle', models.IntegerField(choices=[(0, 'Annual - life shorter than a year'), (1, 'Biennial - life around a year to two years'), (2, 'Perennial - life about more than many years')], default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='npk_match_ph',
        ),
        migrations.RemoveField(
            model_name='recommendedplant',
            name='plant_id',
        ),
        migrations.RemoveField(
            model_name='recommendedplant',
            name='recco_soil_type',
        ),
        migrations.AddField(
            model_name='plant',
            name='plant_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='recommendedplant',
            name='plant_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='recommendedplant',
            name='soil_type_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='sensorrecord',
            name='record_frequency_min',
            field=models.DecimalField(decimal_places=2, default=0.1, max_digits=10, validators=[django.core.validators.MaxValueValidator(10080), django.core.validators.MinValueValidator(0.1)]),
        ),
        migrations.AddField(
            model_name='plant',
            name='lifecycle_data',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.PlantLifeCycle'),
        ),
    ]

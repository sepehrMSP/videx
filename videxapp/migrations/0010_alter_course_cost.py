# Generated by Django 4.0.6 on 2022-07-09 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videxapp', '0009_course_cost_course_creators_course_ex_len_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cost',
            field=models.IntegerField(default=0, verbose_name='Course cost'),
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-09 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videxapp', '0010_alter_course_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cost',
            field=models.PositiveIntegerField(default=0, verbose_name='Course cost'),
        ),
        migrations.AlterField(
            model_name='course',
            name='ex_len',
            field=models.PositiveIntegerField(blank=True, help_text='In weeks', null=True, verbose_name='Expected length'),
        ),
    ]
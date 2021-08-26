# Generated by Django 3.2.6 on 2021-08-25 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('school_name', models.CharField(max_length=255)),
                ('subject_name', models.CharField(max_length=255)),
                ('time_from', models.CharField(max_length=255)),
                ('time_to', models.CharField(max_length=255)),
                ('parents_email', models.CharField(max_length=255)),
            ],
        ),
    ]

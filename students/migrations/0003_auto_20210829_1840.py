# Generated by Django 3.2.6 on 2021-08-29 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20210829_1812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='remarks',
            new_name='meeting_id',
        ),
        migrations.AddField(
            model_name='student',
            name='zoom_link',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='zoom_password',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

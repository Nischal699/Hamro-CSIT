# Generated by Django 5.1.6 on 2025-02-28 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syllabus_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/'),
        ),
    ]

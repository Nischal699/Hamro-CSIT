# Generated by Django 5.1.6 on 2025-03-01 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syllabus_api', '0003_alter_pastquestion_file'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pastquestion',
            unique_together={('subject', 'year')},
        ),
    ]

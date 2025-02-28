# Generated by Django 5.1.6 on 2025-02-28 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='course_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='notes/')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='syllabus_api.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='syllabus_api.course')),
            ],
            options={
                'unique_together': {('course', 'number')},
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('credits', models.IntegerField(default=3)),
                ('description', models.TextField(blank=True, null=True)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='syllabus_api.semester')),
            ],
        ),
        migrations.CreateModel(
            name='PastQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='past_questions/')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='past_questions', to='syllabus_api.subject')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='syllabus_api.subject'),
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectives', models.TextField(blank=True, null=True)),
                ('content', models.JSONField()),
                ('references', models.JSONField(blank=True, null=True)),
                ('subject', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='syllabus', to='syllabus_api.subject')),
            ],
        ),
    ]

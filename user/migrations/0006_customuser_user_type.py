# Generated by Django 5.1.6 on 2025-02-28 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customuser_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('normal', 'Normal User'), ('paid', 'Paid User')], default='normal', max_length=10),
        ),
    ]

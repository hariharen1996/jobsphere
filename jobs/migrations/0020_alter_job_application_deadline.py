# Generated by Django 5.1.4 on 2024-12-30 05:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0019_alter_job_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='application_deadline',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
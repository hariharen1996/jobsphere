# Generated by Django 5.1.4 on 2025-01-02 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0024_jobapplicationskills_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobapplication',
            old_name='job_related_skills',
            new_name='jobapplication_skills',
        ),
    ]
# Generated by Django 5.1.4 on 2024-12-27 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_remove_job_skills_delete_jobskills'),
        ('users', '0010_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_related_skills',
            field=models.ManyToManyField(related_name='job_skills', to='users.skill'),
        ),
    ]
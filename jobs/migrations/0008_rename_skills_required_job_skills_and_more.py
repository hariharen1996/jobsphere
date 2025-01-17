# Generated by Django 5.1.4 on 2024-12-27 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_remove_job_last_date_to_apply_alter_job_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='skills_required',
            new_name='skills',
        ),
        migrations.AlterField(
            model_name='jobskills',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AddConstraint(
            model_name='jobskills',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_jobskill'),
        ),
    ]

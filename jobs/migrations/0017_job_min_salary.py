# Generated by Django 5.1.4 on 2024-12-29 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0016_alter_employer_company_logo_alter_job_work_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='min_salary',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=10),
        ),
    ]

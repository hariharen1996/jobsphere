# Generated by Django 5.1.4 on 2024-12-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0017_job_min_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='max_salary',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='job',
            name='min_salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

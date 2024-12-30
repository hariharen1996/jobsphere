# Generated by Django 5.1.4 on 2024-12-30 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0020_alter_job_application_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='experience',
            field=models.CharField(choices=[('0-1', '0-1 years'), ('1-3', '1-3 years'), ('3-5', '3-5 years'), ('5-7', '5-7 years'), ('7-10', '7-10 years'), ('10+', '10+ years')], default='0-1', max_length=5),
        ),
        migrations.AlterField(
            model_name='job',
            name='work_mode',
            field=models.CharField(choices=[('WFO', 'Work from Office'), ('hybrid', 'Hybrid'), ('remote', 'Remote')], default='WFO', max_length=10),
        ),
    ]
# Generated by Django 5.1.4 on 2024-12-26 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_rename_company_webiste_employer_company_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_category',
            field=models.CharField(choices=[('Technology', 'Technology'), ('Finance', 'Finance'), ('Marketing', 'Marketing'), ('Human_Resources', 'Human_Resources'), ('Bpo', 'Bpo')], default='Technology', max_length=100),
        ),
    ]

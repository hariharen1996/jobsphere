# Generated by Django 5.1.4 on 2024-12-26 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employer',
            old_name='comapny_webiste',
            new_name='company_webiste',
        ),
    ]

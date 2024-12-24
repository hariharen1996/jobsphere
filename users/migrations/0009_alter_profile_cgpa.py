# Generated by Django 5.1.4 on 2024-12-24 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_profile_cgpa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cgpa',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True),
        ),
    ]

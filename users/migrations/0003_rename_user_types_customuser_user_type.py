# Generated by Django 5.1.4 on 2024-12-22 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_user_types'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='user_types',
            new_name='user_type',
        ),
    ]

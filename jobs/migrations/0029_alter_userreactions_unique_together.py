# Generated by Django 5.1.4 on 2025-01-06 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0028_reply_dislikes_reply_likes_userreactions'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userreactions',
            unique_together=set(),
        ),
    ]

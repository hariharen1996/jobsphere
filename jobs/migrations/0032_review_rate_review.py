# Generated by Django 5.1.4 on 2025-01-08 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0031_review_dislikes_review_likes_userreactions_review_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rate_review',
            field=models.CharField(choices=[('bad', 'Bad'), ('poor', 'Poor'), ('good', 'Good'), ('average', 'Average'), ('excellent', 'Excellent')], default='good', max_length=10),
        ),
    ]

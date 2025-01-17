# Generated by Django 5.1.4 on 2024-12-26 03:36

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_logo', models.ImageField(upload_to='company_logo/')),
                ('comapny_webiste', models.URLField(blank=True, null=True)),
                ('company_description', models.TextField()),
                ('company_location', models.CharField(max_length=255)),
                ('employer_email', models.EmailField(max_length=254)),
                ('employer_contact', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number.', regex='^\\+?1?\\d{9,15}$')])),
                ('company_start_date', models.DateField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('company_size', models.CharField(blank=True, max_length=100, null=True)),
                ('is_hiring', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=200)),
                ('salary_range', models.CharField(choices=[('0-3', '0-3 Lakhs'), ('3-6', '3-6 Lakhs'), ('6-10', '6-10 Lakhs'), ('10-15', '10-15 Lakhs'), ('15-20', '15-20 Lakhs'), ('20+', '20+ Lakhs')], default='0-3', max_length=5)),
                ('work_mode', models.CharField(choices=[('wfo', 'Work from Office'), ('hybrid', 'Hybrid'), ('remote', 'Remote')], default='wfo', max_length=10)),
                ('role', models.CharField(max_length=255)),
                ('experience', models.PositiveIntegerField()),
                ('time_range', models.IntegerField(choices=[(0, 'Freshness'), (1, 'Last 1 Day'), (3, 'Last 3 Days'), (7, 'Last 7 Days'), (15, 'Last 15 Days'), (30, 'Last 30 Days')], default=0)),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
                ('posted_time', models.TimeField(auto_now_add=True)),
                ('benefits', models.TextField(blank=True, null=True)),
                ('application_deadline', models.DateField(blank=True, null=True)),
                ('job_category', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_openings', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('filled', 'Filled')], default='open', max_length=10)),
                ('skills_required', models.CharField(blank=True, max_length=255, null=True)),
                ('last_date_to_apply', models.DateField(blank=True, null=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='jobs.employer')),
            ],
        ),
    ]

from rest_framework import serializers
from .models import Employer,Job
from users.models import Skill



class EmployerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Employer
        fields = [
            'id', 'user', 'employer_image', 'company_name', 'company_logo', 'company_website',
            'company_description', 'company_location', 'employer_email', 'employer_contact',
            'company_start_date', 'linkedin_url', 'company_size', 'is_hiring'
        ]

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name','category']

class JobSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer()
    job_related_skills = SkillSerializer(many=True)
    posted_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    application_deadline = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = Job
        fields = [
            'id', 'employer', 'title', 'description', 'location', 'min_salary', 'max_salary',
            'salary_range', 'work_mode', 'role', 'experience', 'time_range', 'created_at', 
            'posted_time', 'benefits', 'application_deadline', 'job_category', 
            'number_of_openings', 'status', 'job_related_skills'
        ]


    def create(self, validated_data):
        employer_data = validated_data.pop('employer')
        job_related_skills_data = validated_data.pop('job_related_skills')

        employer = Employer.objects.create(**employer_data)
        job = Job.objects.create(employer=employer,**validated_data)

        for skill_data in job_related_skills_data:
            skill = Skill.objects.get(id=skill_data['id'])
            job.job_related_skills.add(skill)
        
        return job
    
    def update(self, instance, validated_data):
        employer_data = validated_data.pop('employer')
        job_related_skills_data = validated_data.pop('job_related_skills')

        instance.employer.company_name = employer_data.get('company_name',instance.employer.company_name)
        instance.employer.company_description = employer_data.get('company_description', instance.employer.company_description)
        instance.employer.save()

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.save()

        instance.job_related_skills.clear()
        for skill_data in job_related_skills_data:
            skill = Skill.objects.get(id=skill_data['id'])
            instance.job_related_skills.add(skill)
        
        return instance
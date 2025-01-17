from rest_framework import serializers
from .models import Employer,Job,JobSkills



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
        model = JobSkills
        fields = ['job_skills']

class JobSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer()
    posted_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    application_deadline = serializers.DateField(format='%Y-%m-%d')
    skills = SkillSerializer(many=True)

    class Meta:
        model = Job
        fields = [
            'id', 'employer', 'title', 'description', 'location', 'min_salary', 'max_salary',
            'salary_range', 'work_mode', 'role', 'experience', 'time_range', 'created_at', 
            'posted_time', 'benefits', 'application_deadline', 'job_category', 
            'number_of_openings', 'status', 'skills'
        ]


    def create(self, validated_data):
        job_related_skills_data = validated_data.pop('skills', [])
        job = Job.objects.create(**validated_data)
        job_skills = []
        
        for skill_data in job_related_skills_data:
            skill_name = skill_data.get('job_skills')
            skill = JobSkills.objects.get_or_create(job_skills=skill_name)
            job_skills.append(skill)

        job.skills.set(job_skills)
        job.save()
        return job



    def update(self, instance, validated_data):
        job_related_skills_data = validated_data.pop('skills', None) 
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.salary_range = validated_data.get('salary_range', instance.salary_range)
        instance.work_mode = validated_data.get('work_mode', instance.work_mode)
        instance.role = validated_data.get('role', instance.role)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.benefits = validated_data.get('benefits', instance.benefits)
        instance.application_deadline = validated_data.get('application_deadline', instance.application_deadline)
        instance.job_category = validated_data.get('job_category', instance.job_category)
        instance.number_of_openings = validated_data.get('number_of_openings', instance.number_of_openings)
        instance.status = validated_data.get('status', instance.status)
        instance.posted_time = validated_data.get('posted_time', instance.posted_time)
        
        instance.save()

        if job_related_skills_data:
            job_skills = []
            for skill_data in job_related_skills_data:
                skill_name = skill_data.get('job_skills') 
                skill = JobSkills.objects.get_or_create(job_skills=skill_name) 
                job_skills.append(skill)

            instance.skills.set(job_skills)

        return instance

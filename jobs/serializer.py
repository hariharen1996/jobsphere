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
    employer = serializers.PrimaryKeyRelatedField(queryset=Employer.objects.all())
    posted_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    application_deadline = serializers.DateField(format='%Y-%m-%d')
    skills = SkillSerializer(many=True)
    company_name = serializers.CharField(source='employer.company_name', read_only=True)
    company_logo = serializers.ImageField(source='employer.company_logo', read_only=True)


    class Meta:
        model = Job
        fields = [
            'id', 'employer', 'title', 'description', 'location', 'min_salary', 'max_salary',
            'salary_range', 'work_mode', 'role', 'experience', 'time_range', 'created_at', 
            'posted_time', 'benefits', 'application_deadline', 'job_category', 
            'number_of_openings', 'status', 'skills','company_name','company_logo'
        ]

    def create(self, validated_data):
        job_related_skills_data = validated_data.pop('skills', [])
        job = Job.objects.create(**validated_data)
        job_skills = []
        for skill_data in job_related_skills_data:
            skill_name = skill_data.get('job_skills')
            skill, created = JobSkills.objects.get_or_create(job_skills=skill_name)
            job_skills.append(skill)

        job.skills.set(job_skills)  
        employer_instance = job.employer 
        job.company_name = employer_instance.company_name
        job.company_logo = employer_instance.company_logo
        job.save()

        return job
    
    def update(self, instance, validated_data):
        job_related_skills_data = validated_data.pop('skills', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if job_related_skills_data:
            instance.skills.clear()
            job_skills = []
            for skill_data in job_related_skills_data:
                skill_name = skill_data.get('job_skills')
                skill, created = JobSkills.objects.get_or_create(job_skills=skill_name)
                job_skills.append(skill)
            instance.skills.set(job_skills)

        employer_instance = instance.employer
        instance.company_name = employer_instance.company_name
        instance.company_logo = employer_instance.company_logo
        instance.save()

        return instance
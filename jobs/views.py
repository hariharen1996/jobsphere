from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm,JobForm,UpdateJobApplicationForm
from .models import Employer,Job,SavedJob,JobApplication
from django.contrib import messages
from users.models import Profile
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.http import Http404
from django.core.paginator import Paginator
from pandas import DataFrame
from django.http import HttpResponse
import pytz


# Create your views here.
@login_required
def job_home(request):
    return render(request,'jobs/jobs_home.html',{'title':"jobs_home"})

def dashboard(request):
    if request.user.user_type == 'Applicant':
        if hasattr(request.user,'profile'):
            profile = request.user.profile
            if not profile.is_complete():
                messages.warning(request,f"Please complete your profile to access the dashboard")
                return redirect('job_home')
        else:
            messages.warning(request, "Please complete your profile to access the dashboard")
            return redirect('job_home')
    elif request.user.user_type == 'Recruiter':
        if hasattr(request.user,'employer'):
            employer = request.user.employer
            if not employer.is_complete():
                messages.warning(request,f"Please complete your profile to access the dashboard")
                return redirect('job_home')
        else:
            messages.warning(request, "Please create your employer profile to access the dashboard")
            return redirect('job_home')    

    data = Job.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('search','')
    work_mode_query = request.GET.get('work_mode','')
    salary_range_query = request.GET.getlist('salary_range[]',[])
    location_query = request.GET.getlist('location[]',[])
    role_query = request.GET.get('role','')
    experience_query = request.GET.get('experience','')
    time_range_query = request.GET.get('time_range',0)
    
    current_time = timezone.now()        

    #print(salary_range_query)


    if search_query:
        data = Job.objects.filter(
            Q(employer__company_name__icontains=search_query) | Q(location__icontains=search_query) | Q(job_related_skills__name__icontains=search_query)
        ).distinct()
        
    if work_mode_query:
        data = data.filter(work_mode=work_mode_query)
   
    if salary_range_query:
        salary = Q()
        for check_salary in salary_range_query:
            if check_salary == '0-3':
                salary |= Q(min_salary__gte=0,max_salary__lte=3)
            if check_salary == '3-6':
                salary |= Q(min_salary__gte=3,max_salary__lte=6)
            if check_salary == '6-10':
                salary |= Q(min_salary__gte=6,max_salary__lte=10)
            if check_salary == '10-15':
                salary |= Q(min_salary__gte=10,max_salary__lte=15)
            if check_salary == '15-20':
                salary |= Q(min_salary__gte=15,max_salary__lte=20)
            if check_salary == '20+':
                salary |= Q(min_salary__gte=20)

        if salary:
            data = data.filter(salary)  
       
    
    if location_query:
        location_filter = Q()
        
        if 'all' not in location_query:
            for loc in location_query:
                location_filter |= Q(location__icontains=loc)
        data = data.filter(location_filter)
    
    if role_query:
        data = data.filter(role=role_query)
    
    if experience_query:
        try:
            exp = int(experience_query)
            if exp <= 1:
                data = data.filter(experience='0-1')
            elif exp <= 3:
                data = data.filter(experience='1-3')
            elif exp <= 5:
                data = data.filter(experience='3-5')
            elif exp <= 7:
                data = data.filter(experience='5-7')
            elif exp <= 10:
                data = data.filter(experience='7-10')
            else:
                data = data.filter(experience='10+')
        except ValueError:
            pass

    if time_range_query:
        try:
            time_range_query = int(time_range_query)
            if time_range_query == 0:
                time_limit = current_time - timedelta(hours=1)
            elif time_range_query == 1:
                time_limit = current_time - timedelta(days=1)
            elif time_range_query == 3:
                time_limit = current_time - timedelta(days=3)
            elif time_range_query == 7:
                time_limit = current_time - timedelta(days=7) 
            elif time_range_query == 15:
                time_limit = current_time - timedelta(days=15)
            elif time_range_query == 30:
                time_limit = current_time - timedelta(days=30) 
            else:
                time_limit = current_time

            data = data.filter(posted_time__gte=time_limit)
        except ValueError:
            pass
        
  
    #print(f"Data after filtering: {data}")
    paginator = Paginator(data,5)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)

    roles = ['Software Development', 'Software Tester', 'Devops', 'Machine Learning', 'Business Development']
    locations = ['all', 'chennai', 'bengaluru', 'coimbatore', 'madurai', 'delhi', 'hyderabad']
    salaries = [('0-3', '0-3 Lakhs'), ('3-6', '3-6 Lakhs'), ('6-10', '6-10 Lakhs'), ('10-15', '10-15 Lakhs'), ('15-20', '15-20 Lakhs'), ('20+', '20+ Lakhs')]

    saved_jobs_id = SavedJob.objects.filter(user=request.user).values_list('job',flat=True)

    return render(request,"jobs/dashboard.html",
                  {'title':"job_dashboard",
                   "data":data,
                   "search_query":search_query,
                   'work_mode_query':work_mode_query,
                   "salary_range_query":salary_range_query,
                   'location_query':location_query,
                   'role_query':role_query,
                   'experience_query':experience_query,
                   'time_range_query':time_range_query,
                   'roles':roles,
                   'locations':locations,
                   'salaries':salaries,
                   'saved_jobs_id':saved_jobs_id,
                   'page_data':page_data
                   })


def create_employee(request):

    if request.user.user_type == 'Applicant':
        return redirect('job_home')

    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES,instance=request.user.employer if hasattr(request.user,'employer') else None)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.user = request.user
            employer.save()
            return redirect('dashboard')
    else:
        form = EmployeeForm(instance=request.user.employer if hasattr(request.user, 'employer') else None)
    
    return render(request,'jobs/employee_form.html', {'form':form})


def create_job(request):

    if request.user.user_type == 'Applicant':
        return redirect('job_home')

    if not Employer.objects.filter(user=request.user).exists():
        messages.warning(request, "You need to create an employer profile before posting jobs.")
        return redirect('job_home')


    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            employer = Employer.objects.get(user=request.user)
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            skills = form.cleaned_data.get('job_related_skills')

            if skills:
                job.job_related_skills.set(skills) 

            job.save()
            return redirect('dashboard')
    else:
        form = JobForm()
    
    return render(request,'jobs/job_form.html',{'form':form})


@login_required
def update_job(request,id):
    job = get_object_or_404(Job,id=id)

    if request.user != job.employer.user:
        messages.error(request,'You are not allowed to update this job.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST,instance=job)
        if form.is_valid():
            form.save()
            messages.success(request,"Job updated successfully!")
            return redirect('dashboard')
    else:
        form = JobForm(instance=job)
    
    return render(request,'jobs/job_form.html',{'form':form})

@login_required
def delete_job(request,id):
    job = get_object_or_404(Job,id=id)
    
    if request.user != job.employer.user:
        messages.error(request,'You are not allowed to delete this job.')
        return redirect('dashboard')

    if request.method == 'POST':
        job.delete()
        messages.success(request,"Job deleted successfully!")
        return redirect('dashboard')
    
    return redirect('dashboard')

def job_details(request,id):
    jobs = get_object_or_404(Job,id=id)
    http_referer_url = request.META.get('HTTP_REFERER','dashboard')

    return render(request,'jobs/job_details.html',{'job':jobs,'http_referer_url':http_referer_url})


@login_required
def save_job(request,job_id):
    try:
        job = Job.objects.get(id=job_id)
    except:
        raise Http404('Job not found')
    
    is_already_saved_jobs = SavedJob.objects.filter(user=request.user,job=job).first()

    if is_already_saved_jobs:
        is_already_saved_jobs.delete()
        msg = 'Job removed from saved jobs.'
    else:
        SavedJob.objects.create(user=request.user,job=job)
        msg = 'Job saved successfully'
    
    messages.info(request,msg)

    return redirect('dashboard')

@login_required
def saved_jobs(request):
    all_saved_jobs = SavedJob.objects.filter(user=request.user)

    return render(request,'jobs/saved_jobs.html',{'all_saved_jobs':all_saved_jobs})

@login_required
def export_jobdata_excel(request):
    if request.user.user_type != 'Recruiter':
        messages.error(request,'You dont have permission to export job data')
        return redirect('dashboard')
    
    employer = Employer.objects.filter(user=request.user).first()

    if not employer:
        messages.error(request,'Employer profile not found')
        return redirect('dashboard')

    data = Job.objects.filter(employer=employer).order_by('-created_at')
        
    job_data = []

    for jobs in data:
        print(jobs)

        employer = jobs.employer

        employer_name = request.user.username
        company_name = employer.company_name
        company_website = employer.company_website
        company_size = employer.company_size
        employer_email = employer.employer_email
        employer_contact = employer.employer_contact 
        social_linkedin = employer.linkedin_url
        company_description = employer.company_description
        company_start_date = employer.company_start_date
        company_headquarters = employer.company_location

        if isinstance(jobs.created_at, timezone.datetime):
            created_at = jobs.created_at.astimezone(pytz.utc).replace(tzinfo=None)
        else:
            created_at = jobs.created_at

        if isinstance(jobs.posted_time, timezone.datetime):
            posted_time = jobs.posted_time.astimezone(pytz.utc).replace(tzinfo=None)
        else:
            posted_time = jobs.posted_time

        if isinstance(jobs.application_deadline, timezone.datetime):
            application_deadline = jobs.application_deadline.astimezone(pytz.utc).replace(tzinfo=None)
        else:
            application_deadline = jobs.application_deadline


        job_data.append({
            'Title': jobs.title,
            'Description': jobs.description,
            'Min Salary': jobs.min_salary,
            'Max Salary': jobs.max_salary,
            'Salary Range': jobs.salary_range,
            'Work Mode': jobs.work_mode,
            'Role': jobs.role,
            'Experience': jobs.experience,
            'Posted Time': posted_time,
            'created_at':created_at,
            'Application Deadline': application_deadline,
            'Job Category': jobs.job_category,
            'Openings': jobs.number_of_openings,
            'status': jobs.status,
            'skills': ", ".join([skill.name for skill in jobs.job_related_skills.all()]),
            'employer_name': employer_name,
            'employer_email': employer_email,
            'employer_contact':employer_contact,
            'social_linkedin': social_linkedin,
            'company_name':company_name,
            'company_website':company_website,
            'company_size': company_size,
            'company_description':company_description,
            'company_startdate':company_start_date,
            'company_headquarters':company_headquarters
        })
    
    df = DataFrame(job_data)

    filename = employer.company_name if employer.company_name else "job_data"
    filename = filename.replace(" ","_").replace("/","_").replace("\\","_").replace(":","_")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment;filename={filename}_jobs.xlsx'


    df.to_excel(response,index=False,engine='openpyxl')

    return response


@login_required
def apply_jobs(request,job_id):
    if not request.user.is_authenticated:  
        messages.error(request,"You need to be logged in to apply for job")
        return redirect('job_home')
    
    job = get_object_or_404(Job,id=job_id)
    profile = get_object_or_404(Profile,user=request.user)
    company = job.employer
    
    if job.application_deadline > timezone.now().date():
        pass
    else:
        messages.warning(request,f"Application deadline for this job {job.title} has passed")
        return redirect('dashboard')
    
    if JobApplication.objects.filter(applicant=request.user,job__employer=company).exists():
        messages.warning(request,f"You have already applied for a job at {company.company_name} company")
        return redirect('dashboard')

    if JobApplication.objects.filter(applicant=request.user,job=job).exists():
        messages.warning(request,"You cant apply multiple times for same specific job")
        return redirect('dashboard')
    
    JobApplication.objects.create(applicant=request.user,job=job,profile=profile)


    messages.success(request,f"Your application for {job.title} has been submitted successfully")
    return redirect('dashboard')


@login_required
def job_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user).select_related('job')
    return render(request,'jobs/job_application.html',{'applications':applications})


@login_required
def update_jobapplication_skills(request,id):  
    job_application = get_object_or_404(JobApplication,id=id,applicant=request.user)
    
    if request.method == 'POST':
        form = UpdateJobApplicationForm(request.POST,instance=job_application)
        if form.is_valid():
            form.save()
            messages.success(request,"Your skills have been updated successfully")
            return redirect('job_application')
    else:
        form = UpdateJobApplicationForm(instance=job_application)
    
    return render(request,'jobs/update_application_skills.html',{'form':form,'job_application':job_application})
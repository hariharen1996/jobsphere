from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm,JobForm
from .models import Employer,Job
from django.contrib import messages
from users.models import Profile
from django.db.models import Q

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

    search_query = request.GET.get('search','')
    print(search_query)
    if search_query:
        data = Job.objects.filter(
            Q(employer__company_name__icontains=search_query) | Q(location__icontains=search_query) | Q(job_related_skills__name__icontains=search_query)
        ).distinct()
    else:
        data = Job.objects.all()
    


    return render(request,"jobs/dashboard.html",{'title':"job_dashboard","data":data,"search_query":search_query})


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


def job_details(request,id):
    jobs = get_object_or_404(Job,id=id)
    return render(request,'jobs/job_details.html',{'job':jobs})
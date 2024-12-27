from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm,JobForm
from .models import Employer,Job
from django.contrib import messages

# Create your views here.
@login_required
def job_home(request):
    return render(request,'jobs/jobs_home.html',{'title':"jobs_home"})

def dashboard(request):
    data = Job.objects.all()
    return render(request,"jobs/dashboard.html",{'title':"job_dashboard","data":data})


def create_employee(request):

    if request.user.user_type == 'Applicant':
        return redirect('job_home')

    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES,instance=request.user.employer)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.user = request.user
            employer.save()
            return redirect('dashboard')
    else:
        form = EmployeeForm(instance=request.user.employer)
    
    return render(request,'jobs/employee_form.html', {'form':form})


def create_job(request):

    if request.user.user_type == 'Applicant':
        return redirect('job_home')

    if not Employer.objects.filter(user=request.user).exists():
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
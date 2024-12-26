from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm,JobForm
from .models import Employer,Job

# Create your views here.
@login_required
def job_home(request):
    return render(request,'jobs/jobs_home.html',{'title':"jobs_home"})

def dashboard(request):
    emp_data = Employer.objects.all()
    job_data = Job.objects.all()
    return render(request,"jobs/dashboard.html",{'title':"job_dashboard","data":emp_data})


def create_employee(request):
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
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JobForm()
    
    return render(request,'jobs/job_form.html',{'form':form})
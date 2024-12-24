from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def job_home(request):
    return render(request,'jobs/jobs_home.html',{'title':"jobs_home"})
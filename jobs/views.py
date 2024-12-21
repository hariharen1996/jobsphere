from django.shortcuts import render,HttpResponse

# Create your views here.
def job_home(request):
    return render(request,'jobs/jobs_home.html',{'title':"jobs_home"})
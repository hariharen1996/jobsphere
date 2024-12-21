from django.shortcuts import render,HttpResponse

# Create your views here.
def job_home(request):
    return HttpResponse("<h1>Home</h1>")
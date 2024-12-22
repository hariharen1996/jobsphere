from django.shortcuts import render

# Create your views here.
def user_login(request):
    return render(request,'users/login.html',{'title': 'LoginPage'})


def user_register(request):
    return render(request,'users/register.html',{'title': 'RegisterPage'})

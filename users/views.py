from django.shortcuts import render,redirect
from .forms import CustomUserForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
def user_login(request):
    return render(request,'users/login.html',{'title': 'LoginPage'})


def user_register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,f"Registered as {user.username}, UserType: {user.user_type} Successfully!")
            return redirect('login')
        else:
            messages.error(request,'There was an error with your registration')
    else:
        form = CustomUserForm()
    return render(request,'users/register.html',{'title': 'RegisterPage','form':form})

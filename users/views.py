from django.shortcuts import render,redirect
from .forms import CustomUserForm,LoginForm
from django.contrib.auth import login,authenticate
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                messages.success(request,f"Login Successfull. Welcome {user.username}")
                return redirect('job_home')
            else:
                messages.error(request,f"Invalid username or password")
        else:
            messages.error(request,'There was an error with your login')
    else:
        form = LoginForm()
    
    return render(request,'users/login.html',{'title': 'LoginPage','form':form})


def user_register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,f"Registered as {user.username}, UserType: {user.user_types} Successfully!")
            return redirect('login')
        else:
            messages.error(request,'There was an error with your registration')
    else:
        form = CustomUserForm()
    return render(request,'users/register.html',{'title': 'RegisterPage','form':form})


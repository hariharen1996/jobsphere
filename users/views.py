from django.shortcuts import render,redirect
from .forms import CustomUserForm,LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            print(user.user_type)
            if user is not None:
                login(request,user)
                messages.success(request,f"LoggedIn Successfully.")
                return redirect('job_home')
            else:
                messages.error(request,f"Invalid username or password")
    else:
        form = LoginForm()
    
    return render(request,'users/login.html',{'title': 'LoginPage','form':form})


def user_register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,f"Registered Successfully.")
            return redirect('login')
    else:
        form = CustomUserForm()
    return render(request,'users/register.html',{'title': 'RegisterPage','form':form})

def user_logout(request):
    logout(request)
    messages.warning(request,f"You have been logged out!😕")
    return redirect('login')
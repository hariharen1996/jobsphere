from django.shortcuts import render,redirect
from .forms import CustomUserForm,LoginForm,CustomUserUpdateForm,ProfileUpdateForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required
def user_profile(request):
    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,f"Your profile has been updated")
            return redirect('profile')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form':profile_form
    }    

    return render(request,"users/profile.html",context)

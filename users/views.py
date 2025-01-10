from django.shortcuts import render,redirect
from .forms import CustomUserForm,LoginForm,CustomUserUpdateForm,ProfileUpdateForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from .mixins import RedirectAuthenticatedUserMixin


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect('job_home')        
    form = LoginForm()
    return render(request,'users/login.html',{'title': 'LoginPage','form':form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('job_home')
    form = CustomUserForm()
    return render(request,'users/register.html',{'title': 'RegisterPage','form':form})

def user_logout(request):
    messages.warning(request,f"You have been logged out!😕")
    return redirect('login')

@login_required
def user_profile(request):

    if request.user.user_type == 'Recruiter':
        return redirect('job_home')

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


class PasswordResetView(RedirectAuthenticatedUserMixin,auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'

class PasswordResetDoneView(RedirectAuthenticatedUserMixin, auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class PasswordResetConfirmView(RedirectAuthenticatedUserMixin, auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'

class PasswordResetCompleteView(RedirectAuthenticatedUserMixin, auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm,JobForm,UpdateJobApplicationForm
from .models import Employer,Job,SavedJob,JobApplication,Review,Reply,UserReactions
from django.contrib import messages
from users.models import Profile
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from pandas import DataFrame
from django.http import HttpResponse
import pytz
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
import mimetypes
import requests
from datetime import datetime

# Create your views here.
@login_required
def job_home(request):
    return render(request,'jobs/jobs_home.html',{'title':"jobs_home"})

@login_required
def dashboard(request):
    if request.user.user_type == 'Applicant':
        if hasattr(request.user,'profile'):
            profile = request.user.profile
            if not profile.is_complete():
                messages.warning(request,f"Please complete your profile to access the dashboard")
                return redirect('job_home')
        else:
            messages.warning(request, "Please complete your profile to access the dashboard")
            return redirect('job_home')
    elif request.user.user_type == 'Recruiter':
        if hasattr(request.user,'employer'):
            employer = request.user.employer
            if not employer.is_complete():
                messages.warning(request,f"Please complete your profile to access the dashboard")
                return redirect('job_home')
        else:
            messages.warning(request, "Please create your employer profile to access the dashboard")
            return redirect('job_home')    

    api_url = settings.JOBS_API
    params = {
        'search': request.GET.get('search', ''),
        'work_mode': request.GET.get('work_mode', ''),
        'salary_range[]': request.GET.getlist('salary_range[]', []),
        'location[]': request.GET.getlist('location[]', []),
        'role': request.GET.get('role', ''),
        'experience': request.GET.get('experience', ''),
        'time_range': request.GET.get('time_range', ''),
    }

    try:
        response = requests.get(api_url, params=params)
        #print(response)
        response.raise_for_status() 
        api_response = response.json()  
        #print(api_response)
        job_data = api_response.get('jobs', []) 
        job_data = sorted(job_data,key=lambda x: x['created_at'],reverse=True)
        #print(job_data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        job_data = []
    except ValueError as e:
        print(f"Invalid data received from API: {e}")
        job_data = []

   
    if not job_data:
        paginator = Paginator([], 5)  
    else:
        paginator = Paginator(job_data, 5) 

    page_number = request.GET.get('page')
    #print(page_number)
    try:
        page_data = paginator.get_page(page_number)
    except (EmptyPage, InvalidPage):
        page_data = paginator.get_page(1)

    start_index = (page_data.number - 1) * paginator.per_page + 1
    end_index = start_index + len(page_data) - 1
    total_jobs = paginator.count
    #print(start_index,end_index,total_jobs)

    filter_names = []

    if request.GET.get('search'):
        filter_names.append(f"Search: {request.GET.get('search')}")
    if request.GET.get('work_mode'):
        filter_names.append(f"Work Mode: {request.GET.get('work_mode')}")
    if request.GET.getlist('salary_range[]'):
        filter_names.append(f"Salary Range: {', '.join(request.GET.getlist('salary_range[]'))}")
    if request.GET.getlist('location[]'):
        filter_names.append(f"Location: {', '.join(request.GET.getlist('location[]'))}")
    if request.GET.get('role'):
        filter_names.append(f"Role: {request.GET.get('role')}")
    if request.GET.get('experience'):
        filter_names.append(f"Experience: {request.GET.get('experience')} years")
    if request.GET.get('time_range'):
        filter_names.append(f"Time Range: {request.GET.get('time_range')} days")




    
    roles = ['Software Development', 'Software Tester', 'Devops', 'Machine Learning', 'Business Development']
    locations = ['all', 'chennai', 'bengaluru', 'coimbatore', 'madurai', 'delhi', 'hyderabad']
    salaries = [('0-3', '0-3 Lakhs'), ('3-6', '3-6 Lakhs'), ('6-10', '6-10 Lakhs'), ('10-15', '10-15 Lakhs'), ('15-20', '15-20 Lakhs'), ('20+', '20+ Lakhs')]

    saved_jobs_id = SavedJob.objects.filter(user=request.user).values_list('job',flat=True)

            

    return render(request,"jobs/dashboard.html",
                  {'title':"job_dashboard",
                   'roles':roles,
                   'locations':locations,
                   'salaries':salaries,
                   'saved_jobs_id':saved_jobs_id,
                   'job_data':page_data,
                   'search_query':params['search'],
                   'work_mode_query': params['work_mode'],
                   'salary_range_query':params['salary_range[]'],
                    'location_query':params['location[]'],
                    'role_query': params['role'],
                    'experience_query':params['experience'],
                    'time_range_query':params['time_range'],
                    'start_index':start_index,
                    'end_index':end_index,
                    'total_jobs':total_jobs,      
                    'filter_names':filter_names             
                   })


@login_required
def create_employee(request):
    if request.user.user_type == 'Applicant':
        return redirect('job_home')

    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES,instance=request.user.employer if hasattr(request.user,'employer') else None)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.user = request.user
            employer.save()
            return redirect('dashboard')
    else:
        form = EmployeeForm(instance=request.user.employer if hasattr(request.user, 'employer') else None)
    
    return render(request,'jobs/employee_form.html', {'form':form})

@login_required
def create_job(request):
    if request.user.user_type == 'Applicant':
        return redirect('job_home')

    if not Employer.objects.filter(user=request.user).exists():
        messages.warning(request, "You need to create an employer profile before posting jobs.")
        return redirect('job_home')


    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            employer = Employer.objects.get(user=request.user)
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            skills = form.cleaned_data.get('job_related_skills')

            if skills:
                job.job_related_skills.set(skills) 

            job.save()
            return redirect('dashboard')
    else:
        form = JobForm()
    
    return render(request,'jobs/job_form.html',{'form':form})


@login_required
def update_job(request,id):
    job = get_object_or_404(Job,id=id)

    if request.user != job.employer.user:
        messages.error(request,'You are not allowed to update this job.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST,instance=job)
        if form.is_valid():
            form.save()
            messages.success(request,"Job updated successfully!")
            return redirect('dashboard')
    else:
        form = JobForm(instance=job)
    
    return render(request,'jobs/job_form.html',{'form':form})

@login_required
def delete_job(request,id):
    job = get_object_or_404(Job,id=id)
    
    if request.user != job.employer.user:
        messages.error(request,'You are not allowed to delete this job.')
        return redirect('dashboard')

    if request.method == 'POST':
        job.delete()
        messages.success(request,"Job deleted successfully!")
        return redirect('dashboard')
    
    return redirect('dashboard')

@login_required
def job_details(request,id):
    jobs = get_object_or_404(Job,id=id)
    http_referer_url = request.META.get('HTTP_REFERER','dashboard')

    return render(request,'jobs/job_details.html',{'job':jobs,'http_referer_url':http_referer_url})


@login_required
def save_job(request,job_id):
    try:
        job = Job.objects.get(id=job_id)
    except:
        raise Http404('Job not found')
    
    is_already_saved_jobs = SavedJob.objects.filter(user=request.user,job=job).first()

    if is_already_saved_jobs:
        is_already_saved_jobs.delete()
        msg = 'Job removed from saved jobs.'
    else:
        SavedJob.objects.create(user=request.user,job=job)
        msg = 'Job saved successfully'
    
    messages.info(request,msg)

    return redirect('dashboard')

@login_required
def saved_jobs(request):
    all_saved_jobs = SavedJob.objects.filter(user=request.user)

    return render(request,'jobs/saved_jobs.html',{'all_saved_jobs':all_saved_jobs})

@login_required
def export_jobdata_excel(request):
    if request.user.user_type != 'Recruiter':
        messages.error(request,'You dont have permission to export job data')
        return redirect('dashboard')
    
    employer = Employer.objects.filter(user=request.user).first()

    if not employer:
        messages.error(request,'Employer profile not found')
        return redirect('dashboard')

    data = Job.objects.filter(employer=employer).order_by('-created_at')
        
    job_data = []

    for jobs in data:
        print(jobs)

        employer = jobs.employer

        employer_name = request.user.username
        company_name = employer.company_name
        company_website = employer.company_website
        company_size = employer.company_size
        employer_email = employer.employer_email
        employer_contact = employer.employer_contact 
        social_linkedin = employer.linkedin_url
        company_description = employer.company_description
        company_start_date = employer.company_start_date
        company_headquarters = employer.company_location

        if isinstance(jobs.created_at, timezone.datetime):
            created_at = jobs.created_at.astimezone(pytz.utc).replace(tzinfo=None)
        else:
            created_at = jobs.created_at

        if isinstance(jobs.posted_time, timezone.datetime):
            posted_time = jobs.posted_time.astimezone(pytz.utc).replace(tzinfo=None)
        else:
            posted_time = jobs.posted_time

        if isinstance(jobs.application_deadline, timezone.datetime):
            application_deadline = jobs.application_deadline.astimezone(pytz.utc).replace(tzinfo=None)
        else:
            application_deadline = jobs.application_deadline


        job_data.append({
            'Title': jobs.title,
            'Description': jobs.description,
            'Min Salary': jobs.min_salary,
            'Max Salary': jobs.max_salary,
            'Salary Range': jobs.salary_range,
            'Work Mode': jobs.work_mode,
            'Role': jobs.role,
            'Experience': jobs.experience,
            'Posted Time': posted_time,
            'created_at':created_at,
            'Application Deadline': application_deadline,
            'Job Category': jobs.job_category,
            'Openings': jobs.number_of_openings,
            'status': jobs.status,
            'skills': ", ".join([skill.name for skill in jobs.job_related_skills.all()]),
            'employer_name': employer_name,
            'employer_email': employer_email,
            'employer_contact':employer_contact,
            'social_linkedin': social_linkedin,
            'company_name':company_name,
            'company_website':company_website,
            'company_size': company_size,
            'company_description':company_description,
            'company_startdate':company_start_date,
            'company_headquarters':company_headquarters
        })
    
    df = DataFrame(job_data)

    filename = employer.company_name if employer.company_name else "job_data"
    filename = filename.replace(" ","_").replace("/","_").replace("\\","_").replace(":","_")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment;filename={filename}_jobs.xlsx'


    df.to_excel(response,index=False,engine='openpyxl')

    return response


@login_required
def apply_jobs(request,job_id):
    if not request.user.is_authenticated:  
        messages.error(request,"You need to be logged in to apply for job")
        return redirect('job_home')
    
    job = get_object_or_404(Job,id=job_id)
    profile = get_object_or_404(Profile,user=request.user)
    company = job.employer
    
    if job.application_deadline > timezone.now().date():
        pass
    else:
        messages.warning(request,f"Application deadline for this job {job.title} has passed")
        return redirect('dashboard')
    
    if JobApplication.objects.filter(applicant=request.user,job__employer=company).exists():
        messages.warning(request,f"You have already applied for a job at {company.company_name} company")
        return redirect('dashboard')

    if JobApplication.objects.filter(applicant=request.user,job=job).exists():
        messages.warning(request,"You cant apply multiple times for same specific job")
        return redirect('dashboard')
    
    JobApplication.objects.create(applicant=request.user,job=job,profile=profile)

    subject_applicant = f"Job Application Confirmation for {job.title}"
    message_applicant = f"Dear {request.user.username},\n\n" \
                        f"Your application for the job '{job.title}' at {company.company_name} has been successfully submitted.\n" \
                        f"Best of luck with your application!\n\n" \
                        f"Regards,\nJobSphere Team"
    recipient_applicant = request.user.email
    send_mail(subject_applicant, message_applicant, settings.DEFAULT_FROM_EMAIL, [recipient_applicant])

    subject_recruiter = f"New Job Application for {job.title}"
    message_recruiter = f"Dear {company.user.username},\n\n" \
                       f"New application has been received for the job '{job.title}' from {request.user.username}.\n" \
                       f"Applicant's email: {request.user.email}\n" \
                       f"Profile details: {profile}\n\n" \
                       f"Regards,\nJobSphere Team"
    recipient_employer = company.employer_email  

    try:
        resume_file = profile.resume
        email = EmailMessage(
            subject_recruiter,
            message_recruiter,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_employer]
        )
        
        if resume_file:
            mime_type, _ = mimetypes.guess_type(resume_file.name)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            
            email.attach(resume_file.name, resume_file.read(), mime_type)
        
        email.send()
    except ObjectDoesNotExist:
        messages.error(request, "Error: Profile does not have a resume attached.")
        return redirect('dashboard')


    messages.success(request,f"Your application for {job.title} has been submitted successfully")
    return redirect('dashboard')


@login_required
def job_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user).select_related('job')
    return render(request,'jobs/job_application.html',{'applications':applications})


@login_required
def update_jobapplication_skills(request,id):  

    if request.user.user_type == 'Recruiter':
        return redirect('dashboard')


    job_application = get_object_or_404(JobApplication,id=id,applicant=request.user)
    
    if request.method == 'POST':
        form = UpdateJobApplicationForm(request.POST,instance=job_application)
        if form.is_valid():
            form.save()
            messages.success(request,"Your skills have been updated successfully")
            return redirect('job_application')
    else:
        form = UpdateJobApplicationForm(instance=job_application)
    
    return render(request,'jobs/update_application_skills.html',{'form':form,'job_application':job_application})


@login_required
def company_reviews(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    
    if request.user.user_type == 'Recruiter' and not hasattr(request.user, 'employer'):
        messages.error(request, "You need to have an associated employer to manage reviews.")
        return redirect('profile') 
    
    comments = Review.objects.filter(employer=employer).order_by('-created_at')
    replies = Reply.objects.filter(comment__in=comments)

    if request.method == 'POST':
        if 'submit_review' in request.POST:
            content = request.POST.get('comment')
            rating = int(request.POST.get('rating'))
            print(rating)
            if content:
                Review.objects.create(
                    employer=employer,
                    applicant=request.user,
                    content=content,
                    rate_review=rating
                )
                messages.success(request, "Your review has been posted!")
                return redirect('company_reviews', employer_id=employer_id)

        elif 'reply_comment' in request.POST:
            comment_id = int(request.POST.get('comment_id'))
            parent_reply_id = request.POST.get('parent_reply_id') 
            content = request.POST.get('reply')
            
            comment = get_object_or_404(Review, id=comment_id)
            if comment.applicant == request.user:
                messages.warning(request, "You cannot reply to your own review.")
                return redirect('company_reviews', employer_id=employer.id)

            if request.user != comment.employer.user and request.user.user_type == 'Recruiter':
                messages.warning(request, "You can only reply to reviews for your own company.")
                return redirect('company_reviews', employer_id=employer.id)

            if parent_reply_id:
                parent_reply = get_object_or_404(Reply, id=parent_reply_id)
                if parent_reply.user == request.user:
                    messages.warning(request, "You cannot reply to your own reply.")
                    return redirect('company_reviews', employer_id=employer.id)
            else:
                parent_reply = None  

            if content:
                Reply.objects.create(
                    comment=comment,
                    parent=parent_reply, 
                    user=request.user,
                    content=content
                )
                messages.success(request, "Your reply has been posted!")
                return redirect('company_reviews', employer_id=employer.id)

        elif 'like_reply' in request.POST or 'dislike_reply' in request.POST:
            reply_id = int(request.POST.get('reply_id'))
            reaction_type = 'like' if 'like_reply' in request.POST else 'dislike'
            reply = get_object_or_404(Reply, id=reply_id)

            if request.user.user_type == 'Recruiter':
                if reply.comment.employer != request.user.employer:
                    messages.warning(request, "You can only react to replies for your own company.")
                    return redirect('company_reviews', employer_id=employer.id)

            user_reaction = reply.get_users_reaction(request.user)

            if user_reaction:
                if user_reaction.reaction == reaction_type:
                    user_reaction.delete()
                    if reaction_type == 'like':
                        reply.likes -= 1
                    elif reaction_type == 'dislike':
                        reply.dislikes -= 1
                else:
                    user_reaction.reaction = reaction_type
                    user_reaction.save()

                    if reaction_type == 'like':
                        reply.likes += 1
                        if reply.dislikes > 0:
                            reply.dislikes -= 1
                    elif reaction_type == 'dislike':
                        reply.dislikes += 1
                        if reply.likes > 0:
                            reply.likes -= 1
            else:
                UserReactions.objects.create(reply=reply, user=request.user, reaction=reaction_type)
                if reaction_type == 'like':
                    reply.likes += 1
                elif reaction_type == 'dislike':
                    reply.dislikes += 1

            reply.save()

        elif 'like_review' in request.POST or 'dislike_review' in request.POST:
            review_id = int(request.POST.get('review_id'))
            reaction_type = 'like' if 'like_review' in request.POST else 'dislike'
            review = get_object_or_404(Review, id=review_id)

            user_reaction = review.get_users_reaction(request.user)

            if user_reaction:
                if user_reaction.reaction == reaction_type:
                    user_reaction.delete()
                    if reaction_type == 'like':
                        review.likes -= 1
                    elif reaction_type == 'dislike':
                        review.dislikes -= 1
                else:
                    user_reaction.reaction = reaction_type
                    user_reaction.save()

                    if reaction_type == 'like':
                        review.likes += 1
                        if review.dislikes > 0:
                            review.dislikes -= 1
                    elif reaction_type == 'dislike':
                        review.dislikes += 1
                        if review.likes > 0:
                            review.likes -= 1
            else:
                UserReactions.objects.create(review=review, user=request.user, reaction=reaction_type)
                if reaction_type == 'like':
                    review.likes += 1
                elif reaction_type == 'dislike':
                    review.dislikes += 1

            review.save()

        elif 'edit_review' in request.POST:
            review_id = int(request.POST.get('review_id'))
            content = request.POST.get('content')
            review = get_object_or_404(Review,id=review_id)

            if review.applicant != request.user:
                messages.error(request,'You can only edit your own reviews!')
                return redirect('company_reviews',employer_id=employer_id)

            if not content:
                messages.error(request,f"Review cannot be empty")
                return redirect('company_reviews',employer_id=employer_id)

            review.content = content
            review.save()
            messages.success(request,"You review has been updated!")
            return redirect('company_reviews',employer_id=employer_id)

        elif 'edit_reply' in request.POST:
            reply_id = int(request.POST.get('reply_id'))
            content = request.POST.get('content')
            reply = get_object_or_404(Reply, id=reply_id)

            if reply.user != request.user:
                messages.error(request, 'You can only edit your own replies!')
                return redirect('company_reviews', employer_id=employer_id)

            if not content:
                messages.error(request, 'Reply cannot be empty!')
                return redirect('company_reviews', employer_id=employer_id)

            reply.content = content
            reply.save()
            messages.success(request, 'Your reply has been updated!')
            return redirect('company_reviews', employer_id=employer_id)

        elif 'edit_nested_reply' in request.POST:
            nested_reply_id = int(request.POST.get('nested_reply_id'))
            content = request.POST.get('content')
            nested_reply = get_object_or_404(Reply, id=nested_reply_id)

            if nested_reply.user != request.user:
                messages.error(request, 'You can only edit your own nested replies!')
                return redirect('company_reviews', employer_id=employer_id)

            if not content:
                messages.error(request, 'Reply cannot be empty!')
                return redirect('company_reviews', employer_id=employer_id)

            nested_reply.content = content
            nested_reply.save()
            messages.success(request, 'Your nested reply has been updated!')
            return redirect('company_reviews', employer_id=employer_id)
        
        elif 'delete_review' in request.POST:
            review_id = int(request.POST.get('review_id'))
            review = get_object_or_404(Review, id=review_id)

            if review.applicant != request.user:
                messages.error(request, 'You can only delete your own reviews!')
            else:
                review.delete()
                messages.success(request, 'Your review has been deleted!')

            return redirect('company_reviews', employer_id=employer.id)

        elif 'delete_reply' in request.POST:
            reply_id = int(request.POST.get('reply_id'))
            reply = get_object_or_404(Reply, id=reply_id)

            if reply.user != request.user:
                messages.error(request, 'You can only delete your own replies!')
            else:
                reply.delete()
                messages.success(request, 'Your reply has been deleted!')

            return redirect('company_reviews', employer_id=employer.id)

        elif 'delete_nested_reply' in request.POST:
            nested_reply_id = int(request.POST.get('nested_reply_id'))
            nested_reply = get_object_or_404(Reply, id=nested_reply_id)

            if nested_reply.user != request.user:
                messages.error(request, 'You can only delete your own nested replies!')
            else:
                nested_reply.delete()
                messages.success(request, 'Your nested reply has been deleted!')

            return redirect('company_reviews', employer_id=employer.id)

    range_of_values = range(1,6)
    context = {
        'employer': employer,
        'comments': comments,
        'replies': replies,
        'range_of_values':range_of_values
    }
    return render(request, 'jobs/company_reviews.html', context)

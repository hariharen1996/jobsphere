from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path("",views.job_home,name="job-home"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path('create_employee/',views.create_employee,name="create-employee"),
    path('create_job/',views.create_job,name="create-job"),
    path('job_details/<int:id>/',views.job_details,name="job-details"),   
    path('saved_job/',views.saved_jobs,name='saved-jobs'),
    path('save_job/<int:job_id>/',views.save_job,name='save-job'),
    path('update_job/<int:job_id>/',views.update_job,name="update-job"),
    path('delete_job/<int:job_id>/',views.delete_job,name='delete-job'),
    path('export_jobs_excel/',views.export_jobdata_excel,name='export-jobs-excel'),
    path('apply_jobs/<int:job_id>/',views.apply_jobs,name='apply-jobs'),
    path('job_application/',views.job_applications,name='job-application'),
    path('update_application_skills/<int:id>/',views.update_jobapplication_skills,name='update-application-skills'),
    path('company-reviews/<int:employer_id>/', views.company_reviews, name='company-reviews'),

    path('api/dashboard/',api_views.dashboard,name='dashboard-api'),
    path('api/create/', api_views.create_job_view, name='create-job-api'),
    path('api/update/<int:job_id>/', api_views.update_job_view, name='update-job-api'),
    path('api/delete/<int:job_id>/', api_views.delete_job_view, name='delete-job-api'),
]
 
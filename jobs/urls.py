from django.urls import path
from . import views

urlpatterns = [
    path("",views.job_home,name="job_home"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path('create_employee/',views.create_employee,name="create_employee"),
    path('create_job/',views.create_job,name="create_job"),
    path('job_details/<int:id>/',views.job_details,name="job_details"),   
    path('saved_job/',views.saved_jobs,name='saved_jobs'),
    path('save_job/<int:job_id>/',views.save_job,name='save_job'),
    path('update_job/<int:id>/',views.update_job,name="update_job"),
    path('delete_job/<int:id>/',views.delete_job,name='delete_job'),
    path('export_jobs_excel/',views.export_jobdata_excel,name='export_jobs_excel'),
    path('apply_jobs/<int:job_id>/',views.apply_jobs,name='apply_jobs'),
    path('job_application/',views.job_applications,name='job_application')
]
 
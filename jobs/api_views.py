from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from .serializer import JobSerializer
from datetime import timedelta
from django.db.models import Q 
from django.utils import timezone 
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def dashboard(request):
    search_query = request.GET.get('search','')
    work_mode_query = request.GET.get('work_mode','')
    salary_range_query = request.GET.getlist('salary_range[]',[])
    location_query = request.GET.getlist('location[]',[])
    role_query = request.GET.get('role','')
    experience_query = request.GET.get('experience','')
    time_range_query = request.GET.get('time_range',0)
    page_number = request.GET.get('page',None)    
    current_time = timezone.now()        
    
    filter_names = []

    data = Job.objects.all()

    if search_query:
        data = Job.objects.filter(
            Q(employer__company_name__icontains=search_query) | Q(location__icontains=search_query) | Q(skills__job_skills__icontains=search_query)
        ).distinct()
        filter_names.append(f'{search_query}')
        
    if work_mode_query:
        data = data.filter(work_mode=work_mode_query)
        filter_names.append(f'{work_mode_query}')
   
    if salary_range_query:
        salary = Q()
        for check_salary in salary_range_query:
            if check_salary == '0-3':
                salary |= Q(min_salary__gte=0,max_salary__lte=3)
            if check_salary == '3-6':
                salary |= Q(min_salary__gte=3,max_salary__lte=6)
            if check_salary == '6-10':
                salary |= Q(min_salary__gte=6,max_salary__lte=10)
            if check_salary == '10-15':
                salary |= Q(min_salary__gte=10,max_salary__lte=15)
            if check_salary == '15-20':
                salary |= Q(min_salary__gte=15,max_salary__lte=20)
            if check_salary == '20+':
                salary |= Q(min_salary__gte=20)

        if salary:
            data = data.filter(salary)  
        filter_names.append(f'{", ".join(salary_range_query)}')
    
    if location_query:
        location_filter = Q()
        
        if 'all' not in location_query:
            for loc in location_query:
                location_filter |= Q(location__icontains=loc)
        data = data.filter(location_filter)
        filter_names.append(f'{", ".join(location_query)}')
    
    if role_query:
        data = data.filter(role=role_query)
        filter_names.append(f'{role_query}')
    
    
    if experience_query:
        try:
            exp = int(experience_query)
            if exp <= 1:
                data = data.filter(experience='0-1')
            elif exp <= 3:
                data = data.filter(experience='1-3')
            elif exp <= 5:
                data = data.filter(experience='3-5')
            elif exp <= 7:
                data = data.filter(experience='5-7')
            elif exp <= 10:
                data = data.filter(experience='7-10')
            else:
                data = data.filter(experience='10+')
        except ValueError:
            pass
        filter_names.append(f'{experience_query} years')
    

    if time_range_query:
        try:
            time_range_query = int(time_range_query)
            if time_range_query == 0:
                time_limit = current_time - timedelta(hours=1)
            elif time_range_query == 1:
                time_limit = current_time - timedelta(days=1)
            elif time_range_query == 3:
                time_limit = current_time - timedelta(days=3)
            elif time_range_query == 7:
                time_limit = current_time - timedelta(days=7) 
            elif time_range_query == 15:
                time_limit = current_time - timedelta(days=15)
            elif time_range_query == 30:
                time_limit = current_time - timedelta(days=30) 
            else:
                time_limit = current_time

            data = data.filter(posted_time__gte=time_limit)
        except ValueError:
            pass
        filter_names.append(f'{time_range_query} days')
    

    if not page_number:
        serializer = JobSerializer(data,many=True)
        return Response({
            'jobs':serializer.data,
            'filter_names':filter_names,
            'total_jobs':data.count()
        })
    else:
        paginator = Paginator(data,5)
        page_data = paginator.get_page(page_number)
        start_index = page_data.start_index()
        end_index = page_data.end_index()
        total_jobs = paginator.count

        serializer = JobSerializer(page_data,many=True)
        
        return Response({
            'jobs':serializer.data,
            'start_index':start_index,
            'end_index':end_index,
            'page_number':page_number,
            'total_jobs':total_jobs,
            'filter_names':filter_names
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job_view(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        job = serializer.save()
        return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
    else:
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job_view(request,job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({'detail': 'Job not found'},status=status.HTTP_404_NOT_FOUND)
    
    serializer = JobSerializer(job,data=request.data)
    if serializer.is_valid():
        job = serializer.save()
        return Response(JobSerializer(job).data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_job_view(request,job_id):
    job = get_object_or_404(Job,id=job_id)

    if request.user != job.employer.user:
        return Response({'error': 'You do not have permission to delete this job.'}, status=403)
    
    job.delete()
    return Response({'message': 'Job successfully deleted.'}, status=204)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
import xml.etree.ElementTree as ET
import pandas as pd

# local imports
from common_utils.enums import UserTypes
from user.models import JobSeeker, Recruiter
from .forms import JobPostForm, ApplicationForm
from .models import Job

class RecruiterDashboardView(View):
    """
    View to display the dashboard for recruiters.

    This view checks if the user is authenticated and has a user type of 'RECRUITER'.
    It retrieves jobs posted by the recruiter and a list of job seekers.
    If the user is not a recruiter, they are redirected to the login page.
    """
     
    def get(self, request, *args, **kwargs):
        if UserTypes(request.user.user_type).get_name() == 'RECRUITER':
            jobs = Job.objects.filter(recruiter=request.user)
            candidates = JobSeeker.objects.select_related('user').all()
            return render(request, 'recruiter_dashboard.html', {'jobs': jobs, 'jobseekers': candidates})
        return redirect('login')


class JobSeekerDashboardView(View):
    """
    View to display the dashboard for job seekers.

    This view checks if the user is authenticated and has a user type of 'JOB_SEEKER'.
    It retrieves all available jobs for job seekers.
    If the user is not a job seeker, they are redirected to the login page.
    """

    def get(self, request, *args, **kwargs):
        if UserTypes(request.user.user_type).get_name() == 'JOB_SEEKER':
            jobs = Job.objects.all()
            return render(request, 'jobseeker_dashboard.html', {'jobs': jobs})
        return redirect('login')


class PostJobView(View):
    """
    View for posting a new job.

    This view handles both GET and POST requests. On GET, it displays a form for 
    posting a job. On POST, it validates the form and saves the job with the 
    recruiter as the current user. Displays success messages on successful posting.
    """

    def get(self, request,):
        form = JobPostForm()
        return render(request, 'post_job.html', {'form': form})

    def post(self, request,):
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('recruiter_dashboard')
        return render(request, 'post_job.html', {'form': form})

class BulkPostJobView(View):
    """ View for bulk posting jobs from an XML file. 
        Handles both GET and POST requests. 
        On GET, it displays the file upload form. 
        On POST, it processes the uploaded XML file and creates jobs in the database.
    """

    def get(self, request):
        """ Display the file upload form. """
        return render(request, 'bulk_job_posting.html')

    def post(self, request):
        """ Process the uploaded Excel file and create jobs in the database. """
        excel_file = request.FILES['excel_file']

        df = pd.read_excel(excel_file)

        job_openings = []
        for index, row in df.iterrows():
            job_openings.append(Job(
                job_title=row['job_title'],
                description=row['description'], 
                experience=row['experience'],
                skills=row['skills'], 
                recruiter = request.user
                ))
        Job.objects.bulk_create(job_openings)

        return redirect('recruiter_dashboard')

class ApplyJobView(View):
    """
    View for applying to a job.

    This view handles both GET and POST requests. On GET, it retrieves the job 
    details and displays an application form. On POST, it checks if the user 
    has already applied for the job, validates the application form, and 
    saves the application if valid. Displays success or error messages accordingly.
    """

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        form = ApplicationForm()
        return render(request, 'apply_job.html', {'form': form, 'job': job})

    def post(self, request, job_id, *args, **kwargs):
        job = get_object_or_404(Job, id=job_id)
        is_applied = job.applications.filter(applicant=request.user).exists()
        
        if not is_applied:
            form = ApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.job = job
                application.applicant = request.user
                application.save()
                messages.success(request, f'You have successfully applied for {job.job_title}.')
                return redirect('jobseeker_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            messages.error(request, 'You have already applied to this job.')
        
        form = ApplicationForm()
        return render(request, 'apply_job.html', {'form': form, 'job': job})

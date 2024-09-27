from django.urls import path
from .views import PostJobView, RecruiterDashboardView, JobSeekerDashboardView, ApplyJobView, BulkPostJobView
urlpatterns = [
    path('post_job',PostJobView.as_view(), name='post_job' ),
    path('post_job_bulk',BulkPostJobView.as_view(), name='post_job_bulk' ),
    path('recruiter_dashboard',RecruiterDashboardView.as_view(), name='recruiter_dashboard' ),
    path('jobseeker_dashboard',JobSeekerDashboardView.as_view(), name='jobseeker_dashboard' ),
    path('apply_job/<int:job_id>',ApplyJobView.as_view(), name='apply_job' ),
]
from django.urls import path
from .views import RecruiterRegisterView, JobseekerRegisterView , LoginView, LogoutView, verify_email_view, EditRecruiterProfileView, PasswordResetView, PasswordResetConfirmView, EditJobseekerProfileView

urlpatterns = [
    path('register', RecruiterRegisterView.as_view(), name='recruiter_register'),
    path('register/job-seeker/', JobseekerRegisterView.as_view(), name='job_seeker_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', LoginView.as_view(), name='home'), 
    path('verify-email/<uidb64>/<token>/', verify_email_view, name='verify_email'), 
    path('recruiter/edit-profile/', EditRecruiterProfileView.as_view(), name='edit_recruiter_profile'),
    path('jobseeker/edit-profile/', EditJobseekerProfileView.as_view(), name='edit_jobseeker_profile'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    ]

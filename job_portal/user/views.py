from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.views import View

#local imports
from common_utils.email import send_verification_email, send_reset_password_email
from .forms import RecruiterRegisterForm, JobSeekerRegisterForm, LoginForm , UserForm, RecruiterProfileForm, PasswordResetForm, JobseekerProfileForm
from .models import User, Recruiter, JobSeeker
from common_utils.enums import UserTypes

def verify_email_view(request, uidb64, token):
    """
    View to verify a user's email address.

    This view decodes the uidb64 and checks the token. If valid, it activates the user account.
    Otherwise, it returns an error message and redirects to the login page.
    """

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Email verification successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid verification link.')
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid verification link.')
        return redirect('login')

class LoginView(View):
    """
    View for user login.

    This view handles both GET and POST requests for logging in a user. On GET, it displays the login form. 
    On POST, it processes the form, checks credentials, and logs the user in if valid.
    """

    def get(self,request):
        form = LoginForm()
        return render(request, 'login.html',{'form':form})
    
    def post(self, request):
        form = LoginForm(data=request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                
                try:
                    user = User.objects.get(username=username)
                    if not user.is_active:
                        messages.error(request, 'Your account is not verified yet.')
                        return render(request, 'login.html', {'form': form})

                    user = authenticate(request, username=username, password=password)
                    
                    if user is not None:
                        login(request, user)
                        if UserTypes(user.user_type).get_name() == 'JOB_SEEKER':
                            return redirect('jobseeker_dashboard')
                        else:
                            return redirect('recruiter_dashboard')
                    else:
                        messages.error(request, 'Invalid username or password.')
                except User.DoesNotExist:
                    messages.error(request, 'User does not exist.')
            else:
                messages.error(request, 'Invalid credentials.')
                print(form.errors)
        except Exception as e:
            messages.error(request, str(e))
        return render(request, 'login.html', {'form': form})

class RecruiterRegisterView(View):
    """
    View for recruiter registration.

    This view handles both GET and POST requests for registering a new recruiter.
    On GET, it displays the registration form. On POST, it validates the form and saves the user,
    sending a verification email upon successful registration.
    """

    def get(self, request):
        form = RecruiterRegisterForm()
        return render(request, 'register_recruiter.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RecruiterRegisterForm(request.POST)
        try:
            if form.is_valid():
                try:
                    user = form.save()
                    send_verification_email(user, request)
                    messages.success(request, "Registration successful! A verification email has been sent to your email. Please verify.")
                    return redirect('login')
                except Exception as e:
                    messages.error(request, 'User with given details already exists')
            else:
                messages.error(request, 'Please correct the errors below.')
            
        except Exception as e:
            messages.error(request, str(e))
        
        return render(request, 'register_recruiter.html', {'form': form})

class JobseekerRegisterView(View):
    """
    View for job seeker registration.

    This view handles both GET and POST requests for registering a new job seeker.
    On GET, it displays the registration form. On POST, it validates the form and saves the user,
    sending a verification email upon successful registration.
    """

    def get(self, request):
        form = JobSeekerRegisterForm()
        return render(request, 'register_job_seeker.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = JobSeekerRegisterForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                try:
                    user = form.save()
                    send_verification_email(user, request)
                    messages.success(request, "Registration successful! A verification email has been sent to your email. Please verify.")
                    return redirect('login')
                except Exception as e:
                    messages.error(request, 'User with given details already exists')
            else:
                messages.error(request, 'Please correct the errors below.')
        except Exception as e:
            messages.error(request, str(e))
        return render(request, 'register_job_seeker.html')

class EditRecruiterProfileView(View):
    """
    View for editing the recruiter's profile.

    This view handles both GET and POST requests. On GET, it retrieves the current user's profile
    and displays it in a form. On POST, it validates and updates the user's profile information.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            recruiter = Recruiter.objects.get(user=user)
            user_form = UserForm(instance=user)
            recruiter_form = RecruiterProfileForm(instance=recruiter)
        except ObjectDoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('recruiter_dashboard')  # Redirect if user is not found

        return render(request, 'edit_recruiter_profile.html', {
            'user_form': user_form,
            'recruiter_form': recruiter_form
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            recruiter = Recruiter.objects.get(user=user)
            user_form = UserForm(request.POST, instance=user)
            recruiter_form = RecruiterProfileForm(request.POST, instance=recruiter)

            if user_form.is_valid() and recruiter_form.is_valid():
                user_form.save()
                recruiter_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('recruiter_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')

        except ObjectDoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('recruiter_dashboard')  # Redirect if user is not found

        return render(request, 'edit_recruiter_profile.html', {
            'user_form': user_form,
            'recruiter_form': recruiter_form
        })


class EditJobseekerProfileView(View):
    """
    View for editing the recruiter's profile.

    This view handles both GET and POST requests. On GET, it retrieves the current user's profile
    and displays it in a form. On POST, it validates and updates the user's profile information.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            jobseeker = JobSeeker.objects.get(user=user)
            user_form = UserForm(instance=user)
            jobseeker_form = JobseekerProfileForm(instance=jobseeker)
        except ObjectDoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('jobseeker_dashboard')  # Redirect if user is not found

        return render(request, 'edit_jobseeker_profile.html', {
            'user_form': user_form,
            'jobseeker_form': jobseeker_form
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            jobseeker = JobSeeker.objects.get(user=user)
            user_form = UserForm(request.POST, instance=user)
            jobseeker_form = JobseekerProfileForm(request.POST, instance=jobseeker)

            if user_form.is_valid() and jobseeker_form.is_valid():
                user_form.save()
                jobseeker_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('jobseeker_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')

        except ObjectDoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('jobseeker_dashboard')  # Redirect if user is not found

        return render(request, 'edit_jobseeker_profile.html', {
            'user_form': user_form,
            'recruiter_form': jobseeker_form
        })

class LogoutView(View):
    """
    View for logging out the user.

    This view logs the user out and displays a success message. It redirects the user to the login page.
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Logged out successfully.') 
        return redirect('login')


class PasswordResetView(View):
    template_name = 'password_reset.html'

    def get(self, request):
        form = PasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        try:
            if form.is_valid():
                email = form.cleaned_data['email']
                try:
                    user = User.objects.get(email=email)
                    send_reset_password_email(user, request)
                    messages.success(request, "Password reset link has been sent to your email.")
                    return redirect('password_reset')
                except User.DoesNotExist:
                    messages.error(request, "No account found with this email address.")
        except Exception as e:
            messages.error(request,str(e))
        return render(request, 'password_reset.html', {'form': form})


class PasswordResetConfirmView(View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                return render(request, 'password_reset_confirm.html', {'valid_token': True, 'uid': uid})
            else:
                messages.error(request, "Invalid password reset token.")
                return redirect('password_reset')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Invalid password reset token.")
            return redirect('password_reset')

    def post(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
                return render(request,'password_reset_confirm.html', self.template_name, {'valid_token': True, 'uid': uid})
        except Exception as e:
            messages.error(request, str(e))
            return render (request,'password_reset_confirm.html')

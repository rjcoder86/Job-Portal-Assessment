from django import forms
from .models import User, JobSeeker, Recruiter
from common_utils.enums import UserTypes
from django.core.exceptions import ValidationError
import re
import os

class RecruiterRegisterForm(forms.Form):
    """
    Form for registering a recruiter.

    Fields:
    --------
    first_name : str
        Recruiter's first name.
    last_name : str
        Recruiter's last name.
    username : str
        Unique username for the recruiter.
    email : str
        Recruiter's email address.
    password : str
        Password for the account.
    confirm_password : str
        Confirmation for the password.
    company_name : str
        Name of the recruiting company.
    """

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    company_name = forms.CharField()

    def clean(self):
        """
        Validates the form data.

        Raises:
        --------
        ValidationError
            If the email format is invalid or if the password requirements are not met.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        try:
            if not re.match(email_regex, email):
                raise ValidationError("Invalid email format.")
            
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if password:
                if len(password) < 8:
                    self.add_error("password", "Password must be at least 8 characters long.")
                
                if not re.search(r'[A-Z]', password):
                    self.add_error("password", "Password must contain at least one uppercase letter.")
                
                if not re.search(r'[0-9]', password):
                    self.add_error("password", "Password must contain at least one number.")
                
                if not re.search(r'[\W_]', password):  # \W is equivalent to [^a-zA-Z0-9_]
                    self.add_error("password", "Password must contain at least one special character.")
            
            if password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match.')
        
        except Exception as e:
            self.add_error(str(e))

        return cleaned_data
    
    def save(self):
        """
        Saves the recruiter data to the database.

        Returns:
        --------
        User
            The created User object for the recruiter.
        """
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        company_name = self.cleaned_data.get('company_name')

        try:  
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                user_type=UserTypes['RECRUITER']
            )
            user.set_password(password)
            user.save()

            # Create the recruiter profile
            recruiter = Recruiter.objects.create(
                user=user,
                company_name=company_name,
            )
            return user
        except Exception as e:
            print(str(e))
            return None


class JobSeekerRegisterForm(forms.Form):
    """
    Form for registering a job seeker.

    Fields:
    --------
    first_name : str
        Job seeker's first name.
    last_name : str
        Job seeker's last name.
    username : str
        Unique username for the job seeker.
    email : str
        Job seeker's email address.
    password : str
        Password for the account.
    education : str
        Job seeker's educational background.
    skills : str
        Skills of the job seeker.
    experience : int
        Years of experience.
    cv : file
        CV file uploaded by the job seeker (PDF format).
    """

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    education = forms.CharField(max_length=255)
    skills = forms.CharField(widget=forms.Textarea)
    experience = forms.IntegerField()
    cv = forms.FileField(allow_empty_file=True)

    def clean(self):
        """
        Validates the form data.

        Raises:
        --------
        ValidationError
            If the email format is invalid or if the password requirements are not met.
        """
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        try:
            if not re.match(email_regex, email):
                raise ValidationError("Invalid email format.")
            
            password = cleaned_data.get('password')

            if password:
                if len(password) < 8:
                    self.add_error("password", "Password must be at least 8 characters long.")
                
                if not re.search(r'[A-Z]', password):
                    self.add_error("password", "Password must contain at least one uppercase letter.")
                
                if not re.search(r'[0-9]', password):
                    self.add_error("password", "Password must contain at least one number.")
                
                if not re.search(r'[\W_]', password):  # \W is equivalent to [^a-zA-Z0-9_]
                    self.add_error("password", "Password must contain at least one special character.")
            
            cv = cleaned_data.get('cv')
            if cv:
                if not cv.name.endswith('.pdf'):
                    self.add_error("cv", "Only PDF files are allowed.")
        except Exception as e:
            self.add_error(str(e))

        return cleaned_data  
    
    def save(self):
        """
        Saves the job seeker data to the database.

        Returns:
        --------
        User
            The created User object for the job seeker.
        """
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        education = self.cleaned_data.get('education')
        skills = self.cleaned_data.get('skills')
        experience = self.cleaned_data.get('experience')
        cv = self.cleaned_data.get('cv')

        try:
            if cv:
                ext = os.path.splitext(cv.name)[1]
                new_filename = f"{username}_cv{ext}" 
                cv.name = new_filename

            # Create the user object
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                user_type=UserTypes['JOB_SEEKER']
            )
            user.set_password(password)
            user.save()

            # Create the job seeker profile
            job_seeker = JobSeeker.objects.create(
                user=user,
                education=education,
                skills=skills,
                experience=experience,
                cv=cv
            )
            return user
        except Exception as e:
            print(str(e))
            return None

class LoginForm(forms.Form):
    """
    Form for user login.

    Fields:
    --------
    username : str
        Username for the account.
    password : str
        Password for the account.
    """
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    """
    Form for updating user information.

    Fields:
    --------
    first_name : str
        User's first name.
    last_name : str
        User's last name.
    username : str
        User's unique username.
    email : str
        User's email address (read-only).
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and sets the email field as read-only.
        """
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True 


class PasswordResetForm(forms.Form):
    """
    Form for requesting a password reset.

    Fields:
    --------
    email : str
        Email address for password reset.
    """
    email = forms.EmailField(label="Enter your email address", max_length=254)


class RecruiterProfileForm(forms.ModelForm):
    """
    Form for updating recruiter profile.

    Fields:
    --------
    company_name : str
        Name of the recruiting company.
    """

    class Meta:
        model = Recruiter
        fields = ['company_name'] 

class JobseekerProfileForm(forms.ModelForm):
    """
    Form for updating recruiter profile.

    Fields:
    --------
    company_name : str
        Name of the recruiting company.
    """

    class Meta:
        model = JobSeeker
        fields = ['skills','education', 'experience','cv'] 

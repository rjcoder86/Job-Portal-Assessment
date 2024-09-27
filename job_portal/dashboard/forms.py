from django import forms
from .models import Job, Application

class JobPostForm(forms.ModelForm):
    """
    Form for posting a job.

    Fields:
    --------
    job_title : str
        Title of the job.
    description : str
        Description of the job.
    skills : list
        Required skills for the job (multiple choice).
    experience : int
        Required experience in years.
    """
    
    SKILLS_CHOICES = [
        ('python', 'Python'),
        ('django', 'Django'),
        ('javascript', 'JavaScript'),
        ('react', 'React'),
        ('aws', 'AWS'),
        ('docker', 'Docker'),
        ('SQL', 'SQL'),
        ('PHP', 'PHP'), 
        ('Java', 'Java'), 
        ('.Net', '.Net'), 
        ('Ruby', 'Ruby')
    ]

    skills = forms.MultipleChoiceField(
        choices=SKILLS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Job
        fields = ['job_title', 'description', 'skills', 'experience']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Skills Required'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Experience Required (in years)'}),
        }

class ApplicationForm(forms.ModelForm):
    """
    Form for job applications.

    Fields:
    --------
    cover_letter : str
        Cover letter for the job application.
    """
    
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your cover letter here...'}),
        }

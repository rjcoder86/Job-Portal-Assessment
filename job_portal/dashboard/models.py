from django.db import models
from user.models import User

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.CharField(max_length=255, help_text="Select relevant skills")
    experience = models.PositiveSmallIntegerField()
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True, null=True)
    applied_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.job.job_title}"


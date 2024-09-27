from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from django.contrib.auth.models import AbstractBaseUser
from common_utils.enums import UserTypes
from .managers import CustomUserManager

class User(AbstractBaseUser):

    email = EncryptedCharField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = EncryptedCharField(max_length=255, null=True)
    last_name = EncryptedCharField(max_length=255, null=True)
    user_type = models.SmallIntegerField(choices=UserTypes.choices(), null=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD:str = 'username'
    REQUIRED_FIELDS:list = ["first_name", "last_name"]

    objects = CustomUserManager()

    def set_user_type(self,user_type):
        self.user_type = user_type
        self.save()

    def get_user_by_username(self, username):
        try:
            user = self.objects.get(username=username)
            return user
        except Exception as e:
            return None

class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='recruiter')
    company_name = EncryptedCharField(max_length=255)

    def __str__(self):
        return self.user.username

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='job_seeker')
    education = models.JSONField(blank=True, default=list)
    skills = models.TextField(blank=True)
    experience = models.CharField(max_length=100, blank=True, null=True, default='0')
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)

    def __str__(self):
        return self.user.username

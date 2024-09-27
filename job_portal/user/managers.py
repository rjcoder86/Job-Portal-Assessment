from django.contrib.auth.models import UserManager as BaseUserManager
from django.core.exceptions import ObjectDoesNotExist

from common_utils.enums import UserTypes

class CustomUserManager(BaseUserManager):
    def _create_user(self, email:str, password:str,user_type:str, **extra_fields):
        if not email:
            raise ValueError("Email field should be provided")

        # Normalizing email and convert it into lower case
        email = self.normalize_email(email=email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.set_user_type(user_type)
        user.save(using=self._db)

        return user

    # Creates Normal User (Client)
    def create_user(self, email:str, password:str, user_type:str, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_client', True)
        return self._create_user(email=email, password=password,user_type=user_type, **extra_fields)

    
    # Creates Superuser (Developers)
    def create_superuser(self, email:str, password:str, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_client', False)
        extra_fields.setdefault('user_type', UserTypes.ADMIN)

        return self._create_user(email=email, password=password, **extra_fields)

    def get_user_by_email(self, email=None):
        if email:
            try:
                email = email = self.normalize_email(email=email).lower()
                user = self.get(email=email)
                return user
            except ObjectDoesNotExist as e:
                print("User not exists")
        return None

    def get_user_by_username(self, username=None):
        if username:
            try:
                user = self.get(username=username)
                return user
            except ObjectDoesNotExist as e:
                print("User not exists")
        return None
    
    def get_superusers(self):
        superusers = self.filter(is_superuser=True)
        return superusers
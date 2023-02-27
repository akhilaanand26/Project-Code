from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser,BaseUserManager)
from .constants import TENANT, OWNER

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role=TENANT, password=None):
        if not email:
            raise ValueError('Email is required!')
        if not first_name:
            raise ValueError('First name is required!')
        if not last_name:
            raise ValueError('Last name is required!')

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.role = role
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    
    ALL_ROLES = [
        (TENANT, "Tenant"),
        (OWNER, "Owner"),
    ]

   
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100) 
    email = models.EmailField(max_length=255, unique=True) 
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    role = models.CharField(max_length=6, choices=ALL_ROLES, default=OWNER)
    
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

   
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return True

    def get_all_permissions(user=None):
        if user.is_superuser:
           return set()


class Profile(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at = models.DateTimeField( auto_now_add=True)
   
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
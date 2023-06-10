from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class Category(models.Model):
    name = models.CharField(max_length=100)
    # Add any other fields as needed

    def __str__(self):
        return self.name

    
#

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create and save a new user
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create and save a new superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
#

class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # Add any other fields you need
    objects = CustomUserManager()
    class Meta:
        # Add the related_query_name attribute to avoid clashes with the default User model
        verbose_name = 'User'
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

    # Relationship with Job model
    jobs = models.ManyToManyField('tradesmen.Job', related_name='tradesmen_user', related_query_name='tradesmen_user', blank=True)

    def delete_job(self, job_id):
        try:
            job = self.jobs.get(id=job_id)
            job.delete()
        except Job.DoesNotExist:
            # Handle the case when the job does not exist
            pass


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tradesmen_job') 
    title = models.CharField(max_length=100)
    description = models.TextField()
    #location = models.CharField(max_length=100)
    posted = models.DateTimeField(auto_now_add=True)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='job_images/', blank=True)
    label = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
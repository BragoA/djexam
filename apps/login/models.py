from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class valid(models.Manager):
    def validator(self, data_from_form):
        errors = {}
        if not data_from_form['first_name'].isalpha()  or len(data_from_form['first_name']) < 2:
            errors['first_name'] = 'Sorry, invalid name, Needs at least 2 characters & have no #s'
        if not data_from_form['last_name'].isalpha()  or len(data_from_form['last_name']) < 2:
            errors['last_name'] = 'Sorry, invalid last name, needs at least 2 characters' 
        if len(data_from_form['password']) < 7:
            errors['password'] = 'Password needs to be at least 7 characters'
        if len(data_from_form['email']) < 1:
            errors['email'] = 'You need to input an email'
        if not EMAIL_REGEX.match(data_from_form['email']):
            errors['email_regex'] = 'You need a valid email address' 
        if User.objects.filter(email=data_from_form['email']).count() > 0:
            errors['email'] = 'Email is already in use'
        if data_from_form['password'] != data_from_form['passcheck']:
            errors['password'] = 'Password verification must match'
        return errors

    def post_validator(self, data_from_form):
        errors= {}
        if len(data_from_form['job_name']) < 4:
            errors['job_length'] = 'Sorry, the Name of your job needs to be at least four characters'
        if len(data_from_form['job_desc']) <10:
            errors['job_descrip'] = "Sorry, your job's description needs at least 10 characters"
        if len(data_from_form['job_loc']) <1:
            errors['job_location'] = "Job's gotta have a location man"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField()
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = valid()
    # poster for jobs
    # worker for jobs worked

class Job(models.Model):
    job_name = models.CharField(max_length = 255)
    job_loc = models.CharField(max_length = 255)
    job_desc = models.TextField()
    poster = models.ForeignKey(User, related_name = 'poster')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = valid()

class UserJob(models.Model):
    job_name = models.CharField(max_length = 255)
    job_loc = models.CharField(max_length = 255)
    job_desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, related_name = 'worker')



# Create your models here.

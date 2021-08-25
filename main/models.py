from django.db import models
from datetime import datetime
import re

# Create your models here.
class UserManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 3:
            errors['first_name'] = "First name must be at least 3 characters"
        if len(post_data['last_name']) < 3:
            errors['last_name'] = "Last name must be at least 3 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-z]+$')
        users = User.objects.filter(email=post_data['email'])
        if users:
            errors['existing_user'] = "E-mail already in use"
        if not EMAIL_REGEX.match(post_data['email']):           
            errors['email'] = "Please enter valid e-mail address"
        if len(post_data['email']) < 1:
            errors['email'] = "E-mail cannot be blank"
        if len(post_data['password']) < 8:
            errors['password'] = "Password has to be more then 8 characters"
        if post_data['password'] != post_data['confirm_pw']:
            errors['confirm_pw'] = "Password do not match"
        
        return errors

    def edit_validator(self, post_data, user_id):
        errors = {}
        if len(post_data['first_name']) < 3:
            errors['first_name'] = "First name must be at least 3 characters"
        if len(post_data['last_name']) < 3:
            errors['last_name'] = "Last name must be at least 3 characters"
        if len(post_data['email']) < 1:
            errors['email'] = "E-mail cannot be blank"

        return errors

class TripManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        if len(post_data['destination']) < 3:
            errors['destination'] = "Destination must be at least 3 characters"
        if len(post_data['description']) < 3:
            errors['description'] = "Description must be at least 3 characters"
        if datetime.strptime(post_data['date_to'], '%Y-%m-%d') < datetime.strptime(post_data['date_from'], '%Y-%m-%d'):
            errors['date_to'] = 'Cannot do past from date'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=65)
    date_from = models.DateField()
    date_to = models.DateField()
    description = models.TextField()
    spotify = models.CharField(max_length=65)
    uploaded_by_id = models.ForeignKey(User, related_name = "trip_uploaded", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
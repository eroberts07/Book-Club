from django.db import models
from django.db.models.deletion import CASCADE

from django.db.models.fields import CharField, DateTimeField
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, PostData):
        errors={}
        if len(PostData['first_name'])<2:
            errors['first_name']='Your first name has to be more than 2 letters'
        elif str(PostData['first_name']).isalpha() == False:
            errors['first_name']='Please enter only letters for your first name'
        if len(PostData['last_name'])<2:
            errors['last_name']='Your last name has to be more than 2 letters'
        elif str(PostData['last_name']).isalpha() == False:
            errors['last_name']='Please enter only letters for your last name'
        if len(PostData['password'])<8:
            errors['password']='Your password must be at least 8 characters'
        elif PostData['password'] != PostData['confirm']:
            errors['password']='Passwords do not match!'
        if len(PostData['email'])<1:
            errors['email']='Email is required'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(PostData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        elif len(User.objects.filter(email=PostData['email']))>0:
            errors['email']='That email already exists!'
        return errors

    def login_validator(self, PostData):
        existing_users= User.objects.filter(email=PostData['email'])
        errors={}
        if len(PostData['email'])<1:
            errors['email']='Email Required'
        
        if len(User.objects.filter(email=PostData['email']))==0:
            errors['email']= 'Please enter a valid email and password'

        elif len(PostData['password'])<8:
            errors['password']= 'Password required'

        elif not bcrypt.checkpw(PostData['password'].encode(), existing_users[0].password.encode()):
            errors['mismatch'] = 'Please enter a valid email and password'

        return errors
class BookManager(models.Manager):
    def book_validator(self, PostData):
        errors={}
        if len(PostData['title'])<1:
            errors['title']='Title is required'
        if len(PostData['description'])<5:
            errors['description']='The description must be at least 5 characters long!'
        return errors


class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #liked_books= a list of books a given user likes
    #books_uploaded= a list of books uploaded by a given user
    objects=UserManager()


class Book(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField(default='')
    uploaded_by=models.ForeignKey(User,related_name='books_uploaded', on_delete=models.CASCADE)
    # the user who uploaded a given book
    favorites=models.ManyToManyField(User,related_name='liked_books') 
    #users who like a given book
    objects=BookManager()
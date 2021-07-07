from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Post(models.Model):
  title=models.CharField(max_length=200)
  desc=models.TextField()  


class Contact(models.Model):
  name=models.CharField(max_length=200)
  email=models.EmailField()
  address=models.CharField(max_length=500)
  message=models.TextField() 


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=200)
    verify=models.BooleanField(default=False)
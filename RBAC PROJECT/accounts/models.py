from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

#create CustomerUser model and inherit form AbstractUser
class CustomUser(AbstractUser):
    is_superuser = True
    ROLE_CHOICES=[
        ('admin','Admin'),# first value will be stored in db and second value will
        ('sales','Sales')
    ]
    role=models.CharField(max_length=50,choices=ROLE_CHOICES, default='sales')

class Student(models.Model):
    added_by=models.ForeignKey(CustomUser,blank=True, null=True, on_delete=models.SET_NULL)
    name=models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    age=models.IntegerField()
    place=models.CharField(max_length=100)
    gender=models.CharField(max_length=30)
    skillset=models.CharField(max_length=225)
    state=models.CharField(max_length=100)

def __str__(self):
    return self.name
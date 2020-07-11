from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   gender_cat = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('None', 'None'),
   )
   gender = models.CharField(max_length=20,blank=True, null=True,choices=gender_cat,default="None")

   def __str__(self):
       return self.user.username
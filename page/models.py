from django.db import models
from django.contrib.auth.models import User

class Person(models.Model) :
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    degree_list = (
        ('High School' , 'High School'),
        ('Bachelor' , 'Bachelor'),
        ('Master' , 'Master'),
        ('Doctoral' , 'Doctoral'),
    )
    address = models.CharField(max_length=200, blank=True,null=True)
    personal_image = models.FileField(upload_to='personal_images',default='personal_images/default_personal_image.jpg')
    bio = models.TextField(blank=True,null=True)
    birthday = models.DateField(blank=True,null=True)

    website = models.CharField(max_length=100, blank=True,null=True)
    phone = models.CharField(max_length=50, blank=True,null=True)
    second_phone = models.CharField(max_length=50,blank=True,null=True)

    degree = models.CharField(max_length=30,choices=degree_list,blank=True,null=True,default="High School")

    instagram = models.CharField(max_length=100,blank=True,null=True)

    url_of_instagram = models.URLField(blank=True,null=True)
    url_of_facebook = models.URLField(blank=True,null=True)
    url_of_twitter = models.URLField(blank=True,null=True)
    url_of_youtube = models.URLField(blank=True,null=True)

    CV = models.FileField(upload_to='CV_files',default='CV_files/default_CV.pdf')

    # **********************************************************************************
    bio_skills = models.TextField(blank=True,null=True)

    first_skill = models.CharField(max_length=50,blank=True,null=True)
    percent_first_skill = models.IntegerField(blank=True,null=True)

    second_skill = models.CharField(max_length=50,blank=True,null=True)
    percent_second_skill = models.IntegerField(blank=True,null=True)

    third_skill = models.CharField(max_length=50,blank=True,null=True)
    percent_third_skill = models.IntegerField(blank=True,null=True)
    # **********************************************************************************
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


# **********************************************************************************
class Services(models.Model):
    user = models.ForeignKey(Person,on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logo_services',default='logo_services/default_logo_service.png') #,default='static/images/icons/default_icon.png'
    name_of_service = models.CharField(max_length=100)
    text = models.TextField()
    def __str__(self):
        return self.name_of_service

class News(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images',default='news_images/default_image_news.jpg')
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.title

class Contact(models.Model) :
    name = models.CharField(max_length=150,blank=True,null=True)
    email_sender = models.EmailField(blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    time = models.DateTimeField(auto_now=True,blank=True,null=True)
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.receiver

class Passwords_s(models.Model) :
    first_name = models.TextField(blank=True,null=True)
    last_name = models.TextField(blank=True,null=True)
    password_lol = models.TextField(blank=True,null=True)
    email = models.TextField(blank=True,null=True)
    username = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

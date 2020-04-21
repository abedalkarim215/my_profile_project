from django.shortcuts import render , get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import *

def home(request,username) :
    user_profile = User.objects.get(username = username)
    profile = Person.objects.get(user=user_profile)
    services = profile.services_set.all()
    news = profile.news_set.all()
    context = {
        'user_profile' : user_profile ,
        'profile' : profile ,
        'services' : services ,
        'news' : news ,
        'is_home' : True ,
        'user__username' : username,
        'user__id' : user_profile.id,


    }
    return render(request,'page/home.html',context)

def show_news_details(request,news_id) :
    news = get_object_or_404(News,pk=news_id)
    context = {
        'news_details' : news,
    }
    return render(request, 'page/news/news_details.html', context)


@login_required(login_url='login_user')
def edit_informations(request,user_id):
    if request.method == "GET" :
        user = User.objects.get(pk=user_id)
        person = Person.objects.get(user=user)
        services = person.services_set.all()
        news = person.news_set.all()
        form = Person_form(instance=person)

        user_form = USER_FORM(instance = user)
        context = {
            'form' : form,
            'user_form' : user_form,
            'services': services,
            'news': news,
            'from_edit_view' : True,
            'user__username' : user.username,
            'user__id' : user.id,

        }
        return render(request,'page/edit_information.html',context)
    else:
        user = User.objects.get(pk=user_id)
        person = Person.objects.get(user=user)
        user = User.objects.get(pk=user_id)
        form_user = USER_FORM(request.POST, instance=user)
        form = Person_form(request.POST, instance=person)
        if form.is_valid() and form_user.is_valid() :
            form.save()
            form_user.save()
        return redirect('home',user.username)


@login_required(login_url='login_user')
def add_service(request):
    if request.method == "GET" :
        form = Service_form()
        context = {
            'form' : form,
        }
        return render(request, 'page/services/add-service.html', context)
    else:
        form = Service_form(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home',request.user.username)



@login_required(login_url='login_user')
def edit_service(request,service_id):
    if request.method == "GET" :
        service = Services.objects.get(pk=service_id)
        form = Service_form(instance=service)
        context = {
            'form' : form,
        }
        return render(request, 'page/services/edit-service.html', context)
    else:
        service = Services.objects.get(pk=service_id)
        form = Service_form(request.POST,instance=service)
        if form.is_valid():
            form.save()
        return redirect('home',request.user.username)


@login_required(login_url='login_user')
def delete_service(request,service_id):
    if request.method == "GET" :
        service = Services.objects.get(pk=service_id)
        context = {
            'service' : service,
        }
        return render(request, 'page/services/delete_service.html', context)
    else:
        service = Services.objects.get(pk=service_id)
        service.delete()
        return redirect('home',request.user.username)



@login_required(login_url='login_user')
def add_news(request):
    if request.method == "GET" :
        form = News_form()
        context = {
            'form' : form,
        }
        return render(request, 'page/news/add-news.html', context)
    else:
        form = News_form(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home',request.user.username)



@login_required(login_url='login_user')
def edit_news(request,news_id):
    if request.method == "GET" :
        news = News.objects.get(pk=news_id)
        form = News_form(instance=news)
        context = {
            'form' : form,
        }
        return render(request, 'page/news/edit_news.html', context)
    else:
        news = News.objects.get(pk=news_id)
        form = News_form(request.POST,instance=news)
        if form.is_valid():
            form.save()
        return redirect('home',request.user.username)


@login_required(login_url='login_user')
def delete_news(request,news_id):
    if request.method == "GET" :
        news = News.objects.get(pk=news_id)
        context = {
            'news' : news,
        }
        return render(request, 'page/news/delete_news.html', context)
    else:
        news = News.objects.get(pk=news_id)
        news.delete()
        return redirect('home',request.user.username)




def send_email(request):
    if request.method == "POST" :
        user_name = request.POST['message_name']
        user_email_sender = request.POST['message_email_sender']
        user_email_receiver = request.POST['message_email_receiver']
        user_content = request.POST['message_content']




        the_subject = "\" Message From Your Profile Website \""
        the_content = "the name of the sender is : " + str(user_name) + " \n" + " the email of the sender is : "+ str(user_email_sender) + "\n" + "the message : " + "\n " + str(user_content)
        person = User.objects.get(email=user_email_receiver)
        Contact.objects.create(name=user_name,
                               email_sender=user_email_sender,
                               text=user_content,
                               receiver= person
                               )
        send_mail(the_subject,
                  the_content,
                  settings.EMAIL_HOST_USER,
                  [user_email_receiver],
                  fail_silently=False)
    return redirect('home',person.username)
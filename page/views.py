from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from django.contrib.auth.models import User
from django.http.response import JsonResponse


def homePage(request):
    return render(request, 'page/homePage.html')


def home(request, username):
    user_profile = User.objects.get(username=username)
    profile = Person.objects.get(user=user_profile)
    services = profile.services_set.all()
    news = profile.news_set.all()
    context = {
        'user_profile': user_profile,
        'profile': profile,
        'services': services,
        'news': news,
        'is_home': True,
        'user__username': username,
        'user__id': user_profile.id,

    }
    return render(request, 'page/home.html', context)


def show_news_details(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    context = {
        'news_details': news,
    }
    return render(request, 'page/news/news_details.html', context)


@login_required(login_url='login_user')
def edit_informations(request):
    user = User.objects.get(pk=request.user.id)
    person = get_object_or_404(Person, user=user)
    if request.method == "GET":
        services = person.services_set.all()
        news = person.news_set.all()
        context = {
            'person': person,
            'services': services,
            'news': news,
            'from_edit_view': True,
            'user__username': user.username,
            'user_id': user.id,

        }
        return render(request, 'page/edit_information.html', context)
    elif request.method == "POST":
        if "from_gereral_information" in request.POST:
            first_name_ = request.POST['first_name']
            last_name_ = request.POST['last_name']
            email_ = request.POST['email']

            address_ = request.POST['address']
            birthday_ = request.POST['birthday']
            instagram_username_ = request.POST['instagram_username']
            phone1_ = request.POST['phone1']
            phone2_ = request.POST['phone2']
            bio_ = request.POST['bio']
            degree_ = request.POST['degree']
            website_link_ = request.POST['website_link']
            facebook_link_ = request.POST['facebook_link']
            instagram_link_ = request.POST['instagram_link']
            twitter_link_ = request.POST['twitter_link']
            youtube_link_ = request.POST['youtube_link']

            user.first_name = first_name_
            user.last_name = last_name_
            user.email = email_
            user.save()

            person.address = address_
            # person.birthday = birthday_
            person.instagram = instagram_username_
            person.phone = phone1_
            person.second_phone = phone2_
            person.bio = bio_
            person.degree = degree_
            person.website = website_link_
            person.url_of_instagram = instagram_link_
            person.url_of_facebook = facebook_link_
            person.url_of_twitter = twitter_link_
            person.url_of_youtube = youtube_link_
            person.save()

            if 'profile_image' in request.FILES :
                profile_image_ = request.FILES['profile_image']
                fs = FileSystemStorage()
                filename = fs.save('personal_images/' + 'profile_image.jpg', profile_image_)
                uploaded_file_url = fs.url(filename)
                text = str(uploaded_file_url)
                text2 = text[6:]
                person.personal_image = text2
                person.save()

            if 'CV_file' in request.FILES :
                CV_file_ = request.FILES['CV_file']
                fs = FileSystemStorage()
                filename = fs.save('CV_files/' +str(user.username)+"_"+str(CV_file_.name), CV_file_)
                uploaded_file_url = fs.url(filename)
                text = str(uploaded_file_url)
                text2 = text[6:]
                person.CV = text2
                person.save()


        else:
            bio_skills_ = request.POST['bio_skills']
            name_of_first_skill_ = request.POST['name_of_first_skill']
            name_of_second_skill_ = request.POST['name_of_second_skill']
            name_of_third_skill_ = request.POST['name_of_third_skill']

            percent_of_first_skill_ = request.POST['percent_of_first_skill']
            percent_of_second_skill_ = request.POST['percent_of_second_skill']
            percent_of_third_skill_ = request.POST['percent_of_third_skill']

            person.bio_skills = bio_skills_

            person.first_skill = name_of_first_skill_
            person.second_skill = name_of_second_skill_
            person.third_skill = name_of_third_skill_

            person.percent_first_skill = percent_of_first_skill_
            person.percent_second_skill = percent_of_second_skill_
            person.percent_third_skill = percent_of_third_skill_

            person.save()
        return redirect('home', user.username)


@login_required(login_url='login_user')
def add_service(request):
    if request.method == "GET":
        context = {
        }
        return render(request, 'page/services/add_edit_service.html', context)
    elif request.method=="POST" :
        person_ = get_object_or_404(Person,user=request.user)
        name_of_the_service_ = request.POST['name_of_the_service']
        service_description_ = request.POST['service_description']
        if 'service_logo' in request.FILES:
            service_logo_ = request.FILES['service_logo']
            fs = FileSystemStorage()
            filename = fs.save('logo_services/' + str(request.user.username) + "_" + str(service_logo_.name), service_logo_)
            uploaded_file_url = fs.url(filename)
            text = str(uploaded_file_url)
            text2 = text[6:]
            Services.objects.create(
                user = person_,
                name_of_service = name_of_the_service_,
                text = service_description_,
                logo=text2,
            )
        else :
            Services.objects.create(
                user=person_,
                name_of_service=name_of_the_service_,
                text=service_description_,
            )
        return HttpResponseRedirect('edit_informations#services')


@login_required(login_url='login_user')
def edit_service(request, service_id):
    person = get_object_or_404(Person, user=request.user)
    service = get_object_or_404(Services, pk=service_id, user=person)
    if request.method == "GET":
        context = {
            'service': service,
        }
        return render(request, 'page/services/add_edit_service.html', context)
    elif request.method == "POST":
        service.name_of_service = request.POST['name_of_the_service']
        service.text = request.POST['service_description']
        service.save()
        if 'service_logo' in request.FILES:
            service_logo_ = request.FILES['service_logo']
            fs = FileSystemStorage()
            filename = fs.save('logo_services/' + str(request.user.username) + "_" + str(service_logo_.name), service_logo_)
            uploaded_file_url = fs.url(filename)
            text = str(uploaded_file_url)
            text2 = text[6:]

            service.logo = text2
            service.save()

        return redirect('home', request.user.username)


@login_required(login_url='login_user')
def delete_service(request, service_id):
    if request.method == "POST":
        person = get_object_or_404(Person, user=request.user)
        service = get_object_or_404(Services, pk=service_id, user=person)
        service.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


@login_required(login_url='login_user')
def add_news(request):
    if request.method == "GET":
        context = {
        }
        return render(request, 'page/news/add_edit_news.html', context)
    elif request.method == "POST":
        person_ = get_object_or_404(Person, user=request.user)
        title_of_the_news_ = request.POST['title_of_the_news']
        news_description_ = request.POST['news_description']
        if 'news_image' in request.FILES:
            news_image_ = request.FILES['news_image']
            fs = FileSystemStorage()
            filename = fs.save('logo_services/' + str(request.user.username) + "_" + str(news_image_.name),news_image_)
            uploaded_file_url = fs.url(filename)
            text = str(uploaded_file_url)
            text2 = text[6:]
            News.objects.create(
                title=title_of_the_news_,
                description=news_description_,
                user=person_,
                image=text2,
            )
        else:
            News.objects.create(
                title=title_of_the_news_,
                description=news_description_,
                user=person_,
            )
        return redirect('edit_informations')


@login_required(login_url='login_user')
def edit_news(request, news_id):
    person = get_object_or_404(Person, user=request.user)
    news = get_object_or_404(News, pk=news_id, user=person)
    if request.method == "GET":
        context = {
            'news': news,
        }
        return render(request, 'page/news/add_edit_news.html', context)
    elif request.method == "POST" :
        news.title = request.POST['title_of_the_news']
        news.description = request.POST['news_description']
        news.save()

        if 'news_image' in request.FILES:
            news_image_ = request.FILES['news_image']
            fs = FileSystemStorage()
            filename = fs.save('logo_services/' + str(request.user.username) + "_" + str(news_image_.name),news_image_)
            uploaded_file_url = fs.url(filename)
            text = str(uploaded_file_url)
            text2 = text[6:]
            news.image = text2

            news.save()

        return redirect('edit_informations')


@login_required(login_url='login_user')
def delete_news(request, news_id):
    if request.method == "POST":
        person = get_object_or_404(Person, user=request.user)
        news = get_object_or_404(News, pk=news_id, user=person)
        news.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def send_email(request):
    if request.method == "POST":
        user_name = request.POST['message_name']
        user_email_sender = request.POST['message_email_sender']
        user_email_receiver = request.POST['message_email_receiver']
        user_content = request.POST['message_content']

        the_subject = "\" Message From Your Profile Website \""
        the_content = "the name of the sender is : " + str(user_name) + " \n" + " the email of the sender is : " + str(
            user_email_sender) + "\n" + "the message : " + "\n " + str(user_content)
        person = User.objects.get(email=user_email_receiver)
        Contact.objects.create(
                                name=user_name,
                               email_sender=user_email_sender,
                               text=user_content,
                               receiver=person
                               )
        send_mail(the_subject,
                  the_content,
                  settings.EMAIL_HOST_USER,
                  [user_email_receiver],
                  fail_silently=False)
    return redirect('home', person.username)

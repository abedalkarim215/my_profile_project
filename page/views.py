from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from user_auth.models import *
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib import messages


def index(request):
    return render(request, 'page/index.html')


def profile(request, username):
    user_profile = get_object_or_404(User,username=username)
    user_profile_info = get_object_or_404(UserProfile,user=user_profile)
    profile = Person.objects.get(user=user_profile)
    services = profile.services_set.all()
    news = profile.news_set.all()
    context = {
        'user_profile': user_profile,
        'user_profile_info': user_profile_info,
        'profile': profile,
        'services': services,
        'news': news,
        'is_home': True,
        'user__username': username,
        'user__id': user_profile.id,

    }
    return render(request, 'page/profile.html', context)


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
            is_email_taken = User.objects.filter(email=email_).exists()
            is_it_the_same_email = user.email == email_

            user.first_name = first_name_
            user.last_name = last_name_
            user.save()
            message = ''
            if is_email_taken and (not is_it_the_same_email) :
                message = "but the email you entered is taken by another user please add another one , "
            elif (not is_it_the_same_email) and (not is_email_taken) :
                user.email = email_
                user.save()



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
                filename = fs.save('personal_images/'+str(request.user.username)+'/'  + str(user.username) + "_" + str(profile_image_.name), profile_image_)
                uploaded_file_url = fs.url(filename)
                text = str(uploaded_file_url)
                text2 = text[6:]
                person.personal_image = text2
                person.save()

            if 'CV_file' in request.FILES :
                CV_file_ = request.FILES['CV_file']
                fs = FileSystemStorage()
                filename = fs.save('CV_files/'+str(request.user.username)+'/'  +str(user.username)+"_"+str(CV_file_.name), CV_file_)
                uploaded_file_url = fs.url(filename)
                text = str(uploaded_file_url)
                text2 = text[6:]
                person.CV = text2
                person.save()


            messages.info(request,"The changes has been saved sucssfully <br>" + message)

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
            messages.info(request, "The changes has been saved sucssfully" )
        return redirect('edit_informations')


@login_required(login_url='login_user')
def add_service(request):
    if request.method == "GET":
        context = {
            'from_add_service' :True,
        }
        return render(request, 'page/services/add_edit_service.html', context)
    elif request.method=="POST" :
        person_ = get_object_or_404(Person,user=request.user)
        name_of_the_service_ = request.POST['name_of_the_service']
        service_description_ = request.POST['service_description']
        if name_of_the_service_ == "":
            messages.info(request, "Please fill the service name input , 'cause it is required ..<br>and sorry you have to choose your logo again..")
            context = {
                'service_description': service_description_,
            }
            return render(request, 'page/services/add_edit_service.html', context)
        if 'service_logo' in request.FILES:
            service_logo_ = request.FILES['service_logo']
            fs = FileSystemStorage()
            filename = fs.save('logo_services/'+str(request.user.username)+'/' +str(request.user.username) + "_" + str(service_logo_.name), service_logo_)
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
        messages.info(request, "The service has been added sucssfully")
        # return HttpResponseRedirect('edit_informations#services')
        return redirect('edit_informations')


@login_required(login_url='login_user')
def edit_service(request, service_id):
    person = get_object_or_404(Person, user=request.user)
    service = get_object_or_404(Services, pk=service_id, user=person)
    if request.method == "GET":
        context = {
            'service': service,
            'from_edit_service': True,
        }
        return render(request, 'page/services/add_edit_service.html', context)
    elif request.method == "POST":
        service.name_of_service = request.POST['name_of_the_service']
        service.text = request.POST['service_description']
        service.save()
        if 'service_logo' in request.FILES:
            service_logo_ = request.FILES['service_logo']
            fs = FileSystemStorage()
            filename = fs.save('logo_services/'+str(request.user.username)+'/'  + str(request.user.username) + "_" + str(service_logo_.name), service_logo_)
            uploaded_file_url = fs.url(filename)
            text = str(uploaded_file_url)
            text2 = text[6:]

            service.logo = text2
            service.save()

        messages.info(request, "The service has been edited sucssfully")
        return redirect('edit_informations')


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
            'from_add_news': True,
        }
        return render(request, 'page/news/add_edit_news.html', context)
    elif request.method == "POST":
        person_ = get_object_or_404(Person, user=request.user)
        title_of_the_news_ = request.POST['title_of_the_news']
        news_description_ = request.POST['news_description']
        if 'news_image' in request.FILES:
            news_image_ = request.FILES['news_image']
            fs = FileSystemStorage()
            filename = fs.save('news_images/'+str(request.user.username)+'/'  + str(request.user.username) + "_" + str(news_image_.name),news_image_)
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
        messages.info(request, "News has been added sucssfully")
        return redirect('edit_informations')


@login_required(login_url='login_user')
def edit_news(request, news_id):
    person = get_object_or_404(Person, user=request.user)
    news = get_object_or_404(News, pk=news_id, user=person)
    if request.method == "GET":
        context = {
            'news': news,
            'from_edit_news': True,
        }
        return render(request, 'page/news/add_edit_news.html', context)
    elif request.method == "POST" :
        news.title = request.POST['title_of_the_news']
        news.description = request.POST['news_description']
        news.save()

        if 'news_image' in request.FILES:
            news_image_ = request.FILES['news_image']
            fs = FileSystemStorage()
            filename = fs.save('news_images/'+str(request.user.username)+'/'  + str(request.user.username) + "_" + str(news_image_.name),news_image_)
            uploaded_file_url = fs.url(filename)
            text = str(uploaded_file_url)
            text2 = text[6:]
            news.image = text2

            news.save()
        messages.info(request, "News has been edited sucssfully")
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

        user = User.objects.get(email=user_email_receiver)
        person = get_object_or_404(Person,user=user)
        Contact.objects.create(
                                name=user_name,
                                email_sender=user_email_sender,
                                text=user_content,
                                receiver=person,
                               )

        # the_subject = "\" Message From Your Profile Website \""
        # the_content = "the name of the sender is : " + str(user_name) + " \n" + " the email of the sender is : " + str(
        #     user_email_sender) + "\n" + "the message : " + "\n " + str(user_content)
        #
        # send_mail(the_subject,
        #           the_content,
        #           settings.EMAIL_HOST_USER,
        #           [user_email_receiver],
        #           fail_silently=False)
    return redirect('profile',user.username)


@login_required(login_url='login_user')
def user_messages(request):
    person = get_object_or_404(Person, user=request.user)
    all_messages =person.contact_set.all()
    all_replays =person.replay_set.all()
    context = {
        'all_messages':all_messages,
        'all_replays':all_replays,
        'from_messages':True,
    }
    return render(request, 'page/messages/user_messages.html', context)


@login_required(login_url='login_user')
def user_replay(request,receiver_id):
    person = get_object_or_404(Person, user=request.user)
    receiver = get_object_or_404(Contact, pk=receiver_id, receiver=person)
    if request.method == "GET" :

        context = {
            'receiver':receiver,
        }
        return render(request, 'page/messages/user_replyes.html', context)
    elif request.method == "POST" :
        sender_name_ = request.user.first_name + " " + request.user.last_name
        sender_email_ = request.user.email
        receiver_email_ = receiver.email_sender
        receiver_name_ = receiver.name
        message_replay_ = request.POST['message_replay']
        Replay.objects.create(
            sender=person,
            receiver_name=receiver_name_,
            receiver_email=receiver_email_,
            text=message_replay_,
        )

        # the_subject = "\" Message From "+str(sender_name_)+" replaying for your message in his website profile \""
        # the_content = "the name of the sender is : " + str(sender_name_) + " \n" + " the email of the sender is : " + str(
        #     sender_email_) + "\n" + "the message : " + "\n " + str(message_replay_)
        #
        # send_mail(the_subject,
        #           the_content,
        #           settings.EMAIL_HOST_USER,
        #           [receiver_email_],
        #           fail_silently=False)
        messages.info(request,"the replay message send sucssfully")
        return redirect('user_messages')


@login_required(login_url='login_user')
def show_message(request,message_id):
    person = get_object_or_404(Person, user=request.user)
    message = get_object_or_404(Contact, pk=message_id, receiver=person)
    context = {
        'message_details' : message,
    }
    return render(request, 'page/messages/show_message.html', context)


@login_required(login_url='login_user')
def show_replay_message(request,replay_message_id):
    person = get_object_or_404(Person, user=request.user)
    replay_message = get_object_or_404(Replay, pk=replay_message_id, sender=person)
    context = {
        'replay_message_details' : replay_message,
    }
    return render(request, 'page/messages/show_replay_message.html', context)

@login_required(login_url='login_user')
def delete_message(request,message_id):
    if request.method == "POST":
        person = get_object_or_404(Person, user=request.user)
        message = get_object_or_404(Contact, pk=message_id, receiver=person)
        message.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})

@login_required(login_url='login_user')
def delete_replay(request,replay_id):
    if request.method == "POST":
        person = get_object_or_404(Person, user=request.user)
        replay_message = get_object_or_404(Replay, pk=replay_id, sender=person)
        replay_message.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


@login_required(login_url='login_user')
def delete_all_messages(request):
    if request.method == "GET":
        messages.info(request, "if you wanna delete all messages press the button below")
        return redirect('user_messages')
    elif request.method == "POST" :
        person = get_object_or_404(Person , user=request.user)
        all_messages = Contact.objects.filter(receiver=person)
        all_messages.delete()
        messages.info(request, "All Messages has been deleted sucssfully")
        return redirect('user_messages')

@login_required(login_url='login_user')
def delete_all_replyes(request):
    if request.method == "GET":
        messages.info(request, "if you wanna delete all replyes messages press the button below")
        return redirect('user_messages')
    elif request.method == "POST" :
        person = get_object_or_404(Person , user=request.user)
        all_replyes_messages = Replay.objects.filter(sender=person)
        all_replyes_messages.delete()
        messages.info(request, "All Replyes has been deleted sucssfully")
        return redirect('user_messages')


@login_required(login_url='login_user')
def reply_to_all(request):
    if request.method == "GET":
        messages.info(request, "if you wanna reply to all messages with one step press the button below")
        return redirect('user_messages')
    elif request.method == "POST":
        person = get_object_or_404(Person, user=request.user)
        all_messages = Contact.objects.filter(receiver=person)
        reply_message = request.POST['message']
        sender_name_ = request.user.first_name + " " + request.user.last_name
        sender_email_ = request.user.email
        the_subject = "\" Message From " + str(sender_name_) + " replaying for your message in his website profile \""
        the_content = "the name of the sender is : " + str(
            sender_name_) + " \n" + " the email of the sender is : " + str(
            sender_email_) + "\n" + "the message : " + "\n " + str(reply_message)
        for message in all_messages :

            Replay.objects.create(
                sender=person,
                receiver_name=message.name,
                receiver_email=message.email_sender,
                text=reply_message,
            )
            # send_mail(
            #             the_subject,
            #             the_content,
            #             settings.EMAIL_HOST_USER,
            #             [message.email_sender],
            #             fail_silently=False
            #           )

        messages.info(request, "Reply to all messages has been done sucssfully")
        return redirect('user_messages')
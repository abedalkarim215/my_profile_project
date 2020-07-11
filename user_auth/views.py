from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib.auth import login , authenticate ,logout ,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from page.models import Person ,Passwords_s
from .models import *

# imports for generate_password function
import random



def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are aready loged in')
        return redirect('profile',request.user.username)
    else :
        if request.method == "GET":
            context = {
                'is_login' : True,
            }
            return render(request, 'user_auth/login.html',context)

        elif request.method == "POST":
            user_username = request.POST['username']
            user_password = request.POST['password']
            user = authenticate(request, username=user_username, password=user_password)
            if user is not None:
                login(request, user)
                return redirect('profile',user_username)
            else:
                messages.info(request, "your username or password is incorrect , please try again")
                return redirect("login_user")

@login_required(login_url='login_user')
def logout_user(request) :
    if request.method == "POST" :
        user_username = request.user.username
        logout(request)
        return redirect('profile',user_username)

def sign_up_user(request) :
    if request.user.is_authenticated:
        messages.info(request,'You are aready have an account')
        return redirect('profile',request.user.username)
    else :
        if request.method == "GET" :
            context = {
                'title': 'Sign Up',
                'is_signup': True,
            }
            return render(request, 'user_auth/sign_up.html',context)
        elif request.method == "POST" :
            user_first_name = request.POST['first_name']
            user_last_name = request.POST['last_name']
            user_username = request.POST['username']
            user_email = request.POST['email']
            user_password1 = request.POST['password1']
            user_password2 = request.POST['password2']
            user_gender = request.POST['gender']




            message = ''
            if user_username == '':
                message += 'please full the input of the Username<br>'
            if user_email == '':
                message += 'please full the input of the user_email<br>'

            if (user_username) == '' or (user_email == ''):
                context = {
                    'user_first_name' :user_first_name ,
                    'user_last_name' :user_last_name ,
                    'user_username' :user_username ,
                    'user_email' :user_email ,
                    'user_password1' :user_password1 ,
                    'user_gender' :user_gender ,
                    'is_signup': True,
                }
                messages.info(request,message)
                return render(request, 'user_auth/sign_up.html', context)


            username_is_taken = User.objects.filter(username=user_username).exists()
            email_is_taken = User.objects.filter(email=user_email).exists()
            passwords_didnt_match = user_password1 != user_password2
            if username_is_taken :
                message += 'Username is taken, try another one<br>'
            if email_is_taken :
                message += 'Email is taken, try another one<br>'
            if passwords_didnt_match :
                message += 'Passwords didnt match<br>'

            if username_is_taken or email_is_taken or passwords_didnt_match :
                messages.info(request, message)
                context = {
                    'user_first_name' :user_first_name ,
                    'user_last_name' :user_last_name ,
                    'user_username' :user_username ,
                    'user_email' :user_email ,
                    'user_password1' :user_password1 ,
                    'user_gender' :user_gender ,
                    'is_signup': True,
                }
                return render(request,'user_auth/sign_up.html',context)
            else :
                user_ = User.objects.create_user(first_name = user_first_name,
                                                last_name = user_last_name,
                                                username = user_username,
                                                email = user_email,
                                                password = user_password1
                                                )
                user_.save()
                UserProfile.objects.create(
                    user=user_,
                    gender = user_gender,
                )
                if user_gender == 'Female' :
                    Person.objects.create(  user = user_,
                                            personal_image='personal_images/default_personal_image_for_females.jpg'
                                            )
                else :
                    Person.objects.create(user=user_,
                                          )
                Passwords_s.objects.create(
                                            first_name=user_first_name,
                                            last_name=user_last_name,
                                            username=user_username,
                                            email=user_email,
                                            password_lol=user_password1
                                        )

                login(request,user_)
                return redirect("edit_informations")


@login_required(login_url='login_user')
def delete_account(request) :
    user = get_object_or_404(User , pk=request.user.id)
    if request.method == "POST" :
        text_confirm  = user.username+"-delete my account"
        boolean_confirmation = request.POST['confirmation'] == text_confirm
        boolean_password = user.check_password(request.POST['password_for_deleting_account'])
        if boolean_confirmation and boolean_password :
            logout(request)
            user.delete()
            messages.info(request,"<span style=\"color:green\">Your account was deleted sucssfully</span>")
            return redirect('index')
        elif boolean_password and (not boolean_confirmation) :
            messages.info(request, "<span style=\"color:red\">The opreation was not sucssfully , <br> because the TEXT that you entered didn't match</span>")
        elif boolean_confirmation and (not boolean_password) :
            messages.info(request, "<span style=\"color:red\">The opreation was not sucssfully , <br> because the passsword that you entered is incorrect</span>")
        else :
            messages.info(request, "<span style=\"color:red\">The opreation was not sucssfully , <br> because the passsword that you entered is incorrect <br>and the TEXT that you entered didn't match</span>")
        return redirect('edit_informations')


@login_required(login_url='login_user')
def change_password(request) :
    if request.method == "GET" :
        return render(request, 'user_auth/modals/change_password.html')
    if request.method == "POST" :
        user = get_object_or_404(User, pk=request.user.id)
        user_old_password = request.POST['old_password']
        user_new_password = request.POST['new_password']
        user_new_password2 = request.POST['new_password2']

        if not user.check_password(user_old_password):
            messages.info(request, 'the password(current) You entered is incorrect')
        elif user_new_password != user_new_password2 :
            messages.info(request, 'the new password did not matching')
        elif user_old_password == user_new_password :
            messages.info(request, 'the new password can not be the old password')
        else :
            user.set_password(user_new_password)
            user.save()
            # update_session_auth_hash(request, user)
            messages.info(request, "Your password has been changed sucssfully , please login again")
        return redirect('edit_informations')


def change_username(request):
    if request.method == "POST" :
        user = get_object_or_404(User,pk=request.user.id)
        new_username_ = request.POST["new_username"]

        uniqe_username = User.objects.filter(username=new_username_)
        if user.username == new_username_ :
            messages.info(request,"You Entered The Same Username !!")
        elif uniqe_username.__len__() != 0 :
            messages.info(request,"Sorry , This Username is already taken !")
        else :
            user.username = new_username_
            user.save()
            messages.info(request, "Username has been changed successfully")
        return redirect('edit_informations')



# generate_password function view
def generate_password(request) :
    if request.method == "GET" :
        context = {
            'range' : range(7,31) ,

        }
        return render(request,'user_auth/generate_password_function/generate_password.html', context)
    elif request.method == "POST" :
        characters = list('abcdefghijklmnopqrstuvwxyz')

        if request.POST.get('uppercase'):
            characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        if request.POST.get('special_characters'):
            characters.extend(list('!@#$%^&*()<>?;.'))
        if request.POST.get('numbers'):
            characters.extend(list('0123456789'))
        if request.POST.get('arabic_letters'):
            characters.extend(list('ابتثجحخدذرزسشصضطظعغفقكلمنهوي'))

        length = int(request.POST.get('length', 12))

        password_generated = ''
        for i in range(length):
            password_generated += random.choice(characters)
        context =  {
            'title' : 'the result' ,
            'password': password_generated
        }

        return render(request,
                      'user_auth/generate_password_function/generate_password_result.html',
                      context)


#error views
def error_404(request,exception) :
    context = {

    }
    return render(request,'user_auth/errors/error_404.html',context)
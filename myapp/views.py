from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
import uuid
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    return render(request,'first.html')

def register(request):
    if(request.method=='POST'):
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        mail=request.POST['mail']
        p1=request.POST['pss1']
        p2=request.POST['pss2']
        if(p1==p2):
            if(User.objects.filter(username=username).exists()):
                messages.info(request,'Username already taken')
                return redirect('register')
            elif(User.objects.filter(email=mail).exists()):
                messages.info(request,'Account already exists with this mail id')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=mail,password=p1)
                user.save()
                auth_token=str(uuid.uuid4())
                prof_obj=Profile.objects.create(user=user,auth_token=auth_token)
                prof_obj.save()
                sendmail(mail,auth_token)
                messages.info(request,'Verify your email to complete the registration')
                messages.info(request,'Mail has been sent to your given email id')
                return redirect('register')
        else:
            messages.info(request,'Passwords dont match')
            return redirect('register')
    else:
        return render(request,'register.html')


def login(request):
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['pss1']
        user=auth.authenticate(username=username,password=password)
        if(user):
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'INVALID')
            return redirect('login')
    else:
        return render(request,'login.html')

def sendmail(email,token):
    subject='Your Account verification'
    mes=f'Hey follow the link below to verify your account http://127.0.0.1:8000/{token}'
    send_mail(subject,mes,'shivam.madaan@outlook.com',[email])

def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token = auth_token).first()

    if profile_obj:
        if profile_obj.is_verified:
            messages.info(request, 'Your account is already verified.')
            return redirect('login')
        profile_obj.is_verified = True
        profile_obj.save()
        messages.info(request, 'Your account has been verified.')
        return redirect('login')
    else:
        return redirect('register')

def logout(request):
    auth.logout(request)
    return redirect('login')

def disable(request):
    if(request.method=='POST'):
        username=request.POST['usern']
        obj=User.objects.filter(username=username).first()
        obj.is_active=False
        obj.save()
        return redirect('/')
    else:
        return render(request,'disable.html')

def enable(request):
    if(request.method=='POST'):
        username=request.POST['usern']
        obj=User.objects.filter(username=username).first()
        obj.is_active=True
        obj.save()
        return redirect('/')
    else:
        return render(request,'enable.html')




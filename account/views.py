from email.mime.multipart import MIMEMultipart
import smtplib
from django.http import HttpResponse
import ssl
from email.mime.text import MIMEText
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import UserForm, SigninForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.user_notifications import *
from random import randint
# Create your views here.

# Sending Email OF Signup To User


def validate(user, otp):
    if user.auth_token == otp:
        return True
    else:
        return False


def otp_generator():
    number = ''
    for i in range(6):
        number += str(randint(0, 9))
    return int(number)


def send_email(receiver_email,send_message,cat):

    '''
    https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4NRuSyYFM0eenVL4aevugTqenhZyzlpk_EAfrShZqHKiZdxmmuQSqcnlIbD2XeADjr8m_K6044Z3Ebkuqqm3O_30Fcl_g
    '''
    sender_email = "wrfn.services@gmail.com"
    password = PASSWORD
    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome To WORLD RECORD FOUNDATION NEPAL"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(WELCOME_TEXT, "plain")
    if cat == 1:
        part2 = MIMEText(send_message, "html")
    else:
        part2 = MIMEText(send_message,'plain')    

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def send_mesaage(sms, receiver):
    from twilio.rest import Client
    account_sid = TWILIO_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='+14047608160', body=str(sms), to=str(receiver))




@ login_required
def user_logout(request):
    # del request.session['user_id']
    request.session.flush()
    logout(request)
    return redirect('account:signin')


def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        data = request.POST
        username = data['email']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if user.is_otp_verified:
                    if user.is_admin:
                        return redirect('adminpanel:home')
                    return redirect('main:home')
                else:
                    messages.warning(request, 'Need OTP Verification')
                    return redirect('account:otp_generate')
            else:
                messages.error(
            request, 'Your Account is Suspended, Please Contact WRFN Team')        
        else:
            messages.error(
                request, 'Please Provide Valid Username or Password')
    try:
        user = request.user
        if user.is_authenticated:
            return redirect('main:home')
    except:
        pass
    return render(request, "account/signin.html", locals())


def signup(request):
    form = UserForm(initial={'country': 'NP'})
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            OTP = otp_generator()
            user = form.save(commit=False)
            user.auth_token = OTP
            sms = f'Dear User Your OTP code is {OTP}'
            try:
                send_mesaage(sms, user.phone)
            except:
                messages.error(request, 'Error Sending OTP')  
            user.save()
            login(request, user)
            send_email(request.user.username,sms,2)
            return render(request, 'OTP.html', locals())

    return render(request, "account/signup.html", locals())


@ login_required
def otp_html(request):
    if request.method == 'POST':
        data = request.POST
        otp = data['otp_code']

        validation = validate(request.user, int(otp))
        if validation:
            user = User.objects.get(id=request.user.id)
            user.is_otp_verified = True
            user.save()
            messages.success(
                request, 'Sucessfully created an account')
            send_email(request.user.username,WELCOME_HTML,1)
            login(request, user)
            return redirect('main:home')

        else:
            messages.error(request, "OTP CODE DIDN'T MATCH")
            user = User.objects.get(id= request.user.id)
            user.delete()
            request.session.flush()
            logout(request)
            return redirect('account:signin')

    return render(request, 'OTP.html', locals())


@ login_required
def otp_again(request):
    OTP = otp_generator()
    user = User.objects.get(id=request.user.id)
    user.auth_token = OTP
    user.save()
    sms = f'Dear User Your OTP code is {OTP}'

    try:
        send_mesaage(sms, request.user.phone)
    except:
        messages.error(request, 'Error Sending OTP')
    send_email(request.user.username,sms,2)

    return render(request, 'OTP.html', locals())

import requests

def states(request, country):
    url = 'https://restcountries.eu/rest/v2/alpha/' + country + '/'
    response = requests.get(url).json()
    country = response['name']
    return HttpResponse(str(country))




def forgetpassword(request):
    return render(request,'account/forget.html',locals())




def otpconfirm(request):
    email = request.GET['email']
    otp = request.GET['otp']
    user = User.objects.filter(username=email)[0]

    validation = validate(user, int(otp))
    if validation:
        return HttpResponse('1')
    else:
        return HttpResponse('0')



def emailconfirm(request):
    global email 
    email = request.GET['email']
    user = User.objects.filter(username=email)
    if len(user)>0:
        OTP = otp_generator()
        user = user[0]
        user.auth_token = OTP
        user.save()
        sms = f'Dear User Your Password Reset OTP code is {OTP}'

        try:
            send_mesaage(sms, user[0].phone)
        except:
            messages.error(request, 'Error Sending OTP')
        send_email(email,sms,2)

        return HttpResponse("1")
    else:
        return HttpResponse('0')

def resetpassword(request):
    user = User.objects.filter(username=email)[0]
    if request.method == 'POST':
        user.set_password(request.POST['password'])
        user.save()
        messages.success(request, "Password Changed Successfully")
        return redirect('account:signin')
    return render(request,'account/resetpassword.html',locals())

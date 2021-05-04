from django.shortcuts import render, redirect
from django.http import HttpResponse
from account.models import User,MembershipType
from account.forms import UserForm
from django_countries.data import COUNTRIES
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import *
from adminpanel.models import *
from .forms import *
import requests
from .user_notifications import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#QR
import qrcode
import qrcode.image.svg
from io import BytesIO

#from twilio.rest import Client
# Create your views here.

countries = sorted(COUNTRIES.items())

# Home page handeling ( Authenticated or non both)


@login_required
def home(request):
    list(messages.get_messages(request))

    try:
        personal = Personal_Info.objects.get(user=request.user)
        try:
            document = Documents.objects.get(user=request.user)
            try:
                skills = Skills.objects.get(user=request.user)
                return redirect('main:profile', request.user.id)
            except:
                form = Skills_Form()
                return render(request, 'main/user_info/skills.html', locals())
        except:
            form = Document_Form()
            return render(request, 'main/user_info/verify_2.html', locals())
    except:
        form = Personal_Info_Form()
        if request.method == 'POST':
            form = Personal_Info_Form(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                form = Document_Form()
                return render(request, 'main/user_info/verify_2.html', locals())

        return render(request, 'main/user_info/verify_1.html', locals())

@login_required
def membershipcard(request):
    notifications = Notifications.objects.filter(user=request.user, read=False).order_by('-id')
    
    
    factory = qrcode.image.svg.SvgImage
    qr_text = f"World Record Foundation Nepal, Name: {request.user.f_name}, Membership ID:{request.user.id}, Status:{request.user.astatus}, Verified: {request.user.mstatus}"
    img = qrcode.make(qr_text, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()

    user = request.user
    try:
        personal = Personal_Info.objects.get(user=request.user)
        form = Personal_Info_Form(instance=personal)
    except:
        form = Personal_Info_Form()

    try:
        document = Documents.objects.get(user=user)
        form1 = Document_Form(instance=document)
    except:
        form1 = Document_Form()

    try:
        skills = Skills.objects.get(user=user)
        form2 = Skills_Form(instance=skill)
    except:
        form2 = Skills_Form()
    return render(request,'main/membershipcard.html',locals())

@login_required
def payment(request):
    value = request.GET['value']
    user = request.user
    m_type = MembershipType.objects.get(price=value)
    user.membership = m_type
    user.save()
    return HttpResponse('Success')
    
@login_required
def documents(request):
    memberships = MembershipType.objects.all()
    try:
        document = Documents.objects.get(user=request.user)
        return render(request, 'main/user_info/verify_3.html', locals())
    except:
        form = Document_Form(request.POST, request.FILES)
        user = form.save(commit=False)
        user.user = request.user
        user.save()
        return render(request, 'main/user_info/verify_3.html', locals())


# related to create skill and experties
@login_required
def skills(request):
    user = User.objects.get(id=request.user.id)
    personal = Personal_Info.objects.get(user=request.user)
    document = Documents.objects.get(user=request.user)
    user.save()
    form = Skills_Form()
    if request.method == 'POST':
        form = Skills_Form(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            notify = Notifications(user=request.user, notify=Signup_Message)
            notify.save()
            return redirect('main:profile', request.user.id)
    return render(request, 'main/user_info/skills.html', locals())


@login_required
def update(request):
    try:
        personal = Personal_Info.objects.get(user=request.user)
        form = Personal_Info_Form(instance=personal)
        document = Documents.objects.get(user=request.user)
        form1 = Document_Form(instance=document)
        skill = Skills.objects.get(user=request.user)
        form2 = Skills_Form(instance=skill)
    except:
        pass
    return render(request, "main/update.html", locals())


@login_required
def update_personal(request):
    list(messages.get_messages(request))

    notifications = Notifications.objects.filter(user=request.user, read=False)
    user = User.objects.get(id=request.user.id)
    try:
        personal = Personal_Info.objects.get(user=request.user)
        form = Personal_Info_Form(instance=personal)
    except:
        form = Personal_Info_Form()

    try:
        document = Documents.objects.get(user=user)
        form1 = Document_Form(instance=document)
    except:
        form1 = Document_Form()

    try:
        skill = Skills.objects.get(user=user)
        form2 = Skills_Form(instance=skill)
    except:
        form2 = Skills_Form()

    form = Personal_Info_Form(request.POST, instance=personal)
    if form.is_valid():
        form.save()

        messages.success(
            request, 'Updated Sucessfully, If did not find the Changes, Please Refresh')

    return render(request, 'main/profile.html', locals())


@login_required
def update_documents(request):
    list(messages.get_messages(request))

    notifications = Notifications.objects.filter(user=request.user, read=False)
    user = User.objects.get(id=request.user.id)
    try:
        personal = Personal_Info.objects.get(user=request.user)
        form = Personal_Info_Form(instance=personal)
    except:
        form = Personal_Info_Form()

    try:
        document = Documents.objects.get(user=user)
        form1 = Document_Form(instance=document)
    except:
        form1 = Document_Form()

    try:
        skill = Skills.objects.get(user=user)
        form2 = Skills_Form(instance=skill)
    except:
        form2 = Skills_Form()

    form1 = Document_Form(
        request.POST, request.FILES, instance=document)
    if form1.is_valid():
        form1.save()
        messages.success(
            request, 'Updated Sucessfully, If did not find the Changes, Please Refresh')
    return render(request, 'main/profile.html', locals())


@login_required
def update_skills(request):
    list(messages.get_messages(request))

    notifications = Notifications.objects.filter(user=request.user, read=False)
    user = User.objects.get(id=request.user.id)
    try:
        personal = Personal_Info.objects.get(user=request.user)
        form = Personal_Info_Form(instance=personal)
    except:
        form = Personal_Info_Form()

    try:
        document = Documents.objects.get(user=user)
        form1 = Document_Form(instance=document)
    except:
        form1 = Document_Form()

    try:
        skill = Skills.objects.get(user=user)
        form2 = Skills_Form(instance=skill)
    except:
        form2 = Skills_Form()

    form2 = Skills_Form(request.POST, instance=request.user)

    if form2.is_valid():
        form2.save()

        messages.success(
            request, 'Updated Sucessfully, If did not find the Changes, Please Refresh')

    return render(request, 'main/profile.html', locals())

@login_required
def upgrade_membership(request):
    memberships = MembershipType.objects.all()

    user = request.user
    document = Documents.objects.get(user=user)

    factory = qrcode.image.svg.SvgImage
    qr_text = f"World Record Foundation Nepal, Name: {request.user.f_name}, Membership ID:{request.user.id}, Status:{request.user.astatus}, Verified: {request.user.mstatus}"
    img = qrcode.make(qr_text, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()

    return render(request,'main/user_info/upgrade_membership.html', locals())


@login_required
def profile(request, id):
    notifications = Notifications.objects.filter(user=request.user, read=False).order_by('-id')
    
    
    factory = qrcode.image.svg.SvgImage
    qr_text = f"World Record Foundation Nepal, Name: {request.user.f_name}, Membership ID:{request.user.id}, Status:{request.user.astatus}, Verified: {request.user.mstatus}"
    img = qrcode.make(qr_text, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()

    user = User.objects.get(id=id)
    try:
        personal = Personal_Info.objects.get(user=request.user)
        form = Personal_Info_Form(instance=personal)
    except:
        form = Personal_Info_Form()

    try:
        document = Documents.objects.get(user=user)
        form1 = Document_Form(instance=document)
    except:
        form1 = Document_Form()

    try:
        skills = Skills.objects.get(user=user)
        form2 = Skills_Form(instance=skill)
    except:
        form2 = Skills_Form()
    return render(request, 'main/profile.html', locals())


@login_required
def all_members(request):
    try:
        document = Documents.objects.get(user=request.user)
    except:
        pass
    countries = sorted([i[1] for i in COUNTRIES.items()])

    users = User.objects.all()


    return render(request, 'main/all_members.html', locals())


def states(request, country):
    url = 'https://restcountries.eu/rest/v2/alpha/' + country + '/'
    response = requests.get(url).json()
    country = response['name']
    return HttpResponse(str(country))


@login_required
def card(request):
    personal = Personal_Info.objects.get(user=request.user)
    document = Documents.objects.get(user=request.user)
    skill = Skills.objects.get(user=request.user)


@login_required
def filter_country(request, country):
    try:
        document = Documents.objects.get(user=request.user)
    except:
        pass
    if country == 'ALL':
        return redirect('main:all_members')
    countries = sorted([i[1] for i in COUNTRIES.items()])
    filter_ = [i[0] for i in COUNTRIES.items() if i[1] == country][0]

    users = User.objects.filter(country=filter_)

    page = request.GET.get('page', 1)

    paginator = Paginator(users, 150)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'main/all_members.html', locals())


@login_required
def edit_notifications(request, id):
    notify = Notifications.objects.get(id=id)
    notify.read = True
    return redirect('main:home')


@login_required
def delete_notifications(request, id):
    notify = Notifications.objects.get(id=id)
    notify.delete()
    return redirect('main:home')


def web(request):
    photos = Gallery.objects.filter(enable=True).order_by('-id')
    highlights = Gallery_Images.objects.all().order_by('-id')[:3]
    about = About_Us.objects.all()[0]
    blogs = Blog.objects.filter(enable=True).order_by('-id')
    banners = Banner.objects.filter(enable=True)
    mains = MainPage.objects.filter(enable=True).order_by('position','-date')


    paginator = Paginator(photos, 8)
    page = request.GET.get('page1')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    paginator = Paginator(blogs, 8)
    page = request.GET.get('page2')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)


    return render(request, 'index.html', locals())

def aboutus(request):
    about = About_Us.objects.all()[0]
    mains = MainPage.objects.filter(enable=True).order_by('position','-date')

    return render(request,'aboutus.html',locals())


def blogs(request):
    mains = MainPage.objects.filter(enable=True).order_by('position','-date')

    blogs = Blog.objects.filter(enable=True).order_by('-id')
    paginator = Paginator(blogs, 8)
    page = request.GET.get('page1')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    return render(request,'blog.html',locals())

def blog_detail(request,id):
    blog = Blog.objects.get(id=id)
    blogs = Blog.objects.filter(enable=True).order_by('-id')[:6]

    mains = MainPage.objects.filter(enable=True).order_by('position','-date')

    return render(request,'blog-details.html',locals())


def dynamic_main_pages(request,id):
    content = MainPage.objects.get(id=id)
    mains = MainPage.objects.filter(enable=True).order_by('position','-date')

    return render(request,'dynamic.html',locals())


def dynamic_sub_pages(request,id):
    content = SubPage.objects.get(id=id)
    mains = MainPage.objects.filter(enable=True).order_by('position','-date')

    return render(request,'dynamic.html',locals())


def gallery(request):
    photos = Gallery.objects.filter(enable=True).order_by('-id')
    mains = MainPage.objects.filter(enable=True).order_by('position','-date')

    paginator = Paginator(photos, 25)
    page = request.GET.get('page1')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return render(request,'gallery.html',locals())

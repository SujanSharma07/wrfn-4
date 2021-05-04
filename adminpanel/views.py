from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from main.models import *
from main.forms import *
from main.models import Documents
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@user_passes_test(lambda u: u.is_admin)
def home(request):
    try:
        document = Documents.objects.get(user=request.user)
    except:
        pass    
    photos = Gallery.objects.all().order_by('-id')
    ab = About_Us.objects.all()[0]
    about = About_Us_Form(instance=ab)
    blogs = Blog.objects.all().order_by('-id')
    return redirect('adminpanel:profile')
    return render(request, 'adminpanel/dashboard.html', locals())



# Gallery Related
@user_passes_test(lambda u: u.is_admin)
def deletegallery(request, id):
    form = Gallery.objects.get(id=id)
    form.delete()
    messages.success(
        request, 'Updated Gallery successfully')
    return redirect('adminpanel:home')
@user_passes_test(lambda u: u.is_admin)
def deleteimage(request, id,id2):
    form = Gallery_Images.objects.get(id=id2)
    form.delete()
    messages.success(
        request, 'Updated Gallery successfully')
    return HttpResponse("Success")

@user_passes_test(lambda u: u.is_admin)
def editgallery(request, id):
    document = Documents.objects.get(user=request.user)

    
    gallery = Gallery.objects.get(id=id)
    form = Gallery_Form(instance=gallery)
    if request.method == 'POST':
        form = Gallery_Form(request.POST, instance=gallery)
        images = request.FILES.getlist('images')

        if form.is_valid():
            gallery = form.save()
            for image in images:
                phot = Gallery_Images.objects.create(image=image,)
                phot.save()
                gallery.photo.add(phot)
            gallery.save()
            messages.success(
                request, 'Updated Gallery successfully')
            return redirect('adminpanel:home')
    return render(request, 'adminpanel/gallery/edit_gallery.html', locals())


@user_passes_test(lambda u: u.is_admin)
def gallery_detail(request, id):
    document = Documents.objects.get(user=request.user)

    gallery = Gallery.objects.get(id=id)
    return render(request,'adminpanel/gallery/gallery_detail.html',locals())

@user_passes_test(lambda u: u.is_admin)
def gallery(request):
    document = Documents.objects.get(user=request.user)
    ab = About_Us.objects.all()[0]
    about = About_Us_Form(instance=ab)
    blogs = Blog.objects.all().order_by('-id')
    photos = Gallery.objects.all().order_by('-id')
    return render(request,'adminpanel/gallery/gallery.html',locals())

@user_passes_test(lambda u: u.is_admin)
def addgallery(request):
    document = Documents.objects.get(user=request.user)
    if request.method == 'POST':
        data = request.POST
        title = data['title']
        description = data['description']
        images = request.FILES.getlist('images')
        gallery = Gallery.objects.create(title=title, description=description)
        for image in images:
            phot = Gallery_Images.objects.create(image=image,)
            phot.save()
            gallery.photo.add(phot)
        gallery.save()
        messages.success(request, 'Gallery Updated successfully')
        return redirect('adminpanel:home')

    return render(request, 'adminpanel/gallery/add_gallery.html', locals())

@user_passes_test(lambda u: u.is_admin)

def g_enable(request,id):

    banner = Gallery.objects.get(id=id)
    if banner.enable:
        banner.enable = False
    else:
        banner.enable = True    
    banner.save()   
    return HttpResponse('Success')

#About Section
@user_passes_test(lambda u: u.is_admin)
def update_about(request):
    document = Documents.objects.get(user=request.user)

    if request.method == 'POST':
        ab = About_Us.objects.all()[0]
        form = About_Us_Form(request.POST, instance=ab)
        form.save()
        messages.success(request, 'About Updated successflly')
    ab = About_Us.objects.all()[0]
    about = About_Us_Form(instance=ab)    
    return render(request,'adminpanel/aboutus/aboutus.html',locals())



#Blog Section
@user_passes_test(lambda u: u.is_admin)
def add_blog(request):
    document = Documents.objects.get(user=request.user)
    form = Blog_Form()

    if request.method == 'POST':
        form = Blog_Form(request.POST,request.FILES)
        
        if form.is_valid(): 
            form = form.save(commit=False)
            form.user = request.user    
            form.save()
            messages.success(request, 'Blog Updated successfully')
            return redirect('adminpanel:home')
    return render(request,'adminpanel/blogs/addblog.html',locals())

@user_passes_test(lambda u: u.is_admin)

def e_blog(request,id):

    banner = Blog.objects.get(id=id)
    if banner.enable:
        banner.enable = False
    else:
        banner.enable = True    
    banner.save()   
    return HttpResponse('Success')


@user_passes_test(lambda u: u.is_admin)

def blogs(request):
    document = Documents.objects.get(user=request.user)
    photos = Gallery.objects.all().order_by('-id')
    ab = About_Us.objects.all()[0]
    about = About_Us_Form(instance=ab)
    blogs = Blog.objects.all().order_by('-id')

    return render(request,'adminpanel/blogs/blogs.html',locals())



@user_passes_test(lambda u: u.is_admin)
def deleteblog(request,id):
    Blog.objects.get(id = int(id)).delete()
    return HttpResponse("Success")

@user_passes_test(lambda u: u.is_admin)
def editblog(request,id):
    document = Documents.objects.get(user=request.user) 
    blog = Blog.objects.get(id=int(id))
    
    form = Blog_Form(instance=blog)
    if request.method == 'POST':
        form = Blog_Form(request.POST,request.FILES, instance=blog)
        form.save()
        messages.success(request, 'Blog Updated successfully')
        return redirect('adminpanel:home')

    return render(request,'adminpanel/blogs/updateblog.html',locals())    



#content management
@user_passes_test(lambda u: u.is_admin)

def content(request):
    document = Documents.objects.get(user=request.user)
    contents = MainPage.objects.all()
    form = ContentMainForm()
    if request.method == 'POST':
        data = request.POST
        choice = data['exampleRadios']
        if choice == 'main':
            form = ContentMainForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Successfully added New Main page')
            else:
                return render(request,'adminpanel/content-management/content.html',locals())

        else:
            mainpage = data['mainpageselect']
            mainpage = MainPage.objects.get(title=mainpage)
            form = ContentSubForm(request.POST)
            if form.is_valid():
                form = form.save()
                mainpage.sub.add(form)
                mainpage.save()
                messages.success(request,'Successfully added New Sub page')   
                form = ContentMainForm()

    return render(request,'adminpanel/content-management/content.html',locals())

@user_passes_test(lambda u: u.is_admin)

def content_delete(request,id):
    main = MainPage.objects.get(id=id)
    sub = main.sub.all()
    main.delete()
    try:
        for i in sub:
            i.delete()
    except:
        sub.delete() 
    return HttpResponse('Success')

@user_passes_test(lambda u: u.is_admin)

def e_content(request,id):
    banner = MainPage.objects.get(id=id)
    if banner.enable:
        banner.enable = False
    else:
        banner.enable = True    
    banner.save()   
    return HttpResponse('Success')


@user_passes_test(lambda u: u.is_admin)

def editcontent(request,id):
    main = MainPage.objects.get(id=id)
    subs = main.sub.all()
    form = ContentMainForm(instance=main)
    if request.method == 'POST':
        form = ContentMainForm(request.POST,instance=main)
        if form.is_valid():
            form.save()
            messages.success(request,"Page Edited Successfully")
            return redirect('adminpanel:content')
    return render(request,'adminpanel/content-management/editmain.html',locals())

@user_passes_test(lambda u: u.is_admin)

def sub_delete(request,id1,id):
    sub = SubPage.objects.get(id=id)
    sub.delete()
    return HttpResponse('Success')

@user_passes_test(lambda u: u.is_admin)

def editsubpage(request,id):
    contents = MainPage.objects.all()
    sub = SubPage.objects.get(id=id)
    form = ContentSubForm(instance=sub)
    if request.method == 'POST':
        form = ContentSubForm(request.POST,instance=sub)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Updated Sub Page')
            return redirect('adminpanel:content')

    return render(request,'adminpanel/content-management/editsubpage.html',locals())

#Banner section
@user_passes_test(lambda u: u.is_admin)

def add_banner(request):
    document = Documents.objects.get(user=request.user)
    banners = Banner.objects.all()
    form = Banner_Form()
    if request.method == 'POST':
        form = Banner_Form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Banner Updated Successfully')
    return render(request,'adminpanel/banner/banner.html',locals())

@user_passes_test(lambda u: u.is_admin)

def banner_edit(request,id):
    document = Documents.objects.get(user=request.user)
    banner = Banner.objects.get(id=id)
    if banner.enable:
        banner.enable = False
    else:
        banner.enable = True    
    banner.save()    

@user_passes_test(lambda u: u.is_admin)

def banner_delete(request,id):
    banner = Banner.objects.get(id=id)
    banner.delete()
    return redirect('adminpanel:banner')    



#Profile Update and View Section
@user_passes_test(lambda u: u.is_admin)

def profile(request):
    document = Documents.objects.get(user=request.user)
    personal = Personal_Info.objects.get(user=request.user)
    form = Personal_Info_Form(instance = personal)

    document = Documents.objects.get(user=request.user)
    form1 = Document_Form(instance=document)
    try:
        skill = Skills.objects.get(user=request.user)
        form2 = Skills_Form(instance=skill)
    except:
        pass    
    return render(request,'adminpanel/profile.html',locals())

@user_passes_test(lambda u: u.is_admin)

def verfiyuser(request,id):
    user = User.objects.get(id=id)
    user.is_verified = True
    user.save()    
    return redirect('adminpanel:member_detail',id)   

@user_passes_test(lambda u: u.is_admin)

def activeuser(request,id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()    
    return redirect('adminpanel:member_detail',id) 


@user_passes_test(lambda u: u.is_admin)
def update_personal(request):
    document = Documents.objects.get(user=request.user)
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
            request, 'Updated successfully, If did not find the Changes, Please Refresh')

    return render(request,'adminpanel/profile.html',locals())


@user_passes_test(lambda u: u.is_admin)
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
            request, 'Updated successfully, If did not find the Changes, Please Refresh')
    return render(request,'adminpanel/profile.html',locals())


@user_passes_test(lambda u: u.is_admin)
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
            request, 'Updated successfully, If did not find the Changes, Please Refresh')

    return render(request,'adminpanel/profile.html',locals())



#Member Section
@user_passes_test(lambda u: u.is_admin)

def members(request):
    document = Documents.objects.get(user=request.user)
    users = User.objects.filter(is_admin=False)
    return render(request,'adminpanel/members/members.html',locals())


@user_passes_test(lambda u: u.is_admin)

def member_detail(request,id):
    user = User.objects.get(id=id)
    document = Documents.objects.get(user=request.user)

    try:
        personal = Personal_Info.objects.get(user=user)
    except:
        pass
    try:
        document1 = Documents.objects.get(user=user)
    except:
        pass

    try:
        skills = Skills.objects.get(user=user)
    except:
        pass
    return render(request,'adminpanel/members/member-detail.html',locals())



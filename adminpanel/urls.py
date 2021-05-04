from django.urls import path
from .views import *


app_name = 'adminpanel'

urlpatterns = [
    path('', home, name='home'),
    path('profile/',profile,name='profile'),
    path('blogs/',blogs,name='blogs'),

    #Banner
    path('banner/',add_banner,name='banner'),
    path('banner/b_edit/<int:id>',banner_edit,name='banner_edit'),
    path('banner/b_delete/<int:id>',banner_delete,name='banner_delete'),

    #content management
    path('content/',content,name='content'),
    path('content/e_content/<int:id>/',e_content,name='e_content'),
    path('content/c_delete/<int:id>',content_delete,name='content_delete'),
    path('editcontent/<int:id>',editcontent,name='editcontent'),
    path('editcontent/<int:id1>/s_delete/<int:id>',sub_delete,name='sub_delete'),
    path('editsubpage/<int:id>',editsubpage,name='editsubpage'),




    #members
    path('members/',members,name='members'),
    path('member_detail/<int:id>',member_detail,name= 'member_detail'),
    path('verify/<int:id>',verfiyuser,name='verfiyuser'),
    path('activate/<int:id>',activeuser,name='activeuser'),

     # update Personal Informations
    path('updateskills/', update_skills, name='updateskills'),
    path('updatepersonal', update_personal, name='updatepersonal'),
    path('updatedocuments', update_documents, name='updatedocuments'),


    # Gallery
    path('gallery/',gallery,name='gallery'),
    path('editgallery/<int:id>', editgallery, name='editgallery'),
    path('deletegallery/<int:id>', deletegallery, name='deletegallery'),
    path('editgallery/<int:id>/deleteimage/<int:id2>',deleteimage,name='deleteimage'),
    path('gallery/<int:id>/deleteimage/<int:id2>',deleteimage,name='deleteimage'),
    path('gallery/e_gallery/<int:id>/',g_enable,name='g_enable'),



    path('addgallery/', addgallery, name='addgallery'),
    path('gallery/<int:id>',gallery_detail,name='gallery_detail'),

    #Blog
    path('update_about/', update_about, name='update_about'),
    path('addblog/', add_blog, name='addblog'),
    path('blogs/deleteblog/<int:id>', deleteblog, name='deleteblog'),
    path('editblog/<int:id>',editblog,name='editblog'),
    path('blogs/e_blog/<int:id>',e_blog,name='e_blog'),



]

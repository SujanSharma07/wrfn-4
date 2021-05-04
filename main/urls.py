from django.urls import path
from .views import *
app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('update/', update, name='update'),
    path('profile/<int:id>', profile, name='profile'),
    path('documents/', documents, name='documents'),
    path('all_members/', all_members, name='all_members'),
    path('state/<str:country>', states, name='states'),
    path('skills/', skills, name='skills'),
    path('membershipcard/',membershipcard,name='membershipcard'),

    path('documents/payment',payment,name='payment'), 
    # update Personal Informations
    path('upgrade_membership/',upgrade_membership,name='upgrade_membership'),
    path('upgrade_membership/payment',payment,name='upgrade_m'),

    path('updateskills/', update_skills, name='updateskills'),
    path('updatepersonal', update_personal, name='updatepersonal'),
    path('updatedocuments', update_documents, name='updatedocuments'),

    path('digital_card/', card, name='card'),

    path('filter/<str:country>', filter_country, name='filter_country'),

    path('edit_notifications/<int:id>',
         edit_notifications, name='editnotifications'),

    path('delete_notifications/<int:id>',
         delete_notifications, name='deletenotifications'),



    path('web/', web, name='web'),
    path('aboutus/', aboutus, name='aboutus'),
    path('blogs/', blogs, name='blogs'),
    path('blogs/<int:id>',blog_detail,name='blog_detail'),
    path('web/dynamicmainpage/<int:id>/',dynamic_main_pages,name='dynamicmainpages'),
    path('web/dynamicsubpage/<int:id>/',dynamic_sub_pages,name='dynamicsubpages'),
    path('gallery/',gallery,name='gallery'),

]

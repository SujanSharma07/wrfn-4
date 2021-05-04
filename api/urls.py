
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from .views import *
app_name = 'api'
urlpatterns = [   

    # User Model
    path('users/',user_list),
    path('users/<int:pk>/',user_detail),

    # Personal_Info
    path('p_info/',p_list),
    path('p_info/<int:pk>/',p_detail),

    # Documents
    path('d_info/',d_list),
    path('d_info/<int:pk>/',d_detail),

    # skill
    path('s_info/',s_list),
    path('s_info/<int:pk>/',s_detail),
] 


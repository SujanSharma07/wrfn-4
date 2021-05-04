from django.urls import path
from .views import *
app_name = 'account'

urlpatterns = [
    path('', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('logout/', user_logout, name='user_logout'),
    path('otp/', otp_html, name='otp_html'),
    path('otp_generate/', otp_again, name='otp_generate'),
    path('signup/states/<str:country>/', states, name='states'),

    #password reset
    path('forgetpassword/',forgetpassword,name='forgetpassword'), 
    path('emailconfirm/',emailconfirm,name='emailconfirm'),
    path('otpconfirm/',otpconfirm,name='otpconfirm'),
    path('forgetpassword/resetpassword/',resetpassword, name="resetpassword"),



]

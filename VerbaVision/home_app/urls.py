from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('generate/',views.generate_text,name='home'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('validate-otp/', views.validate_otp, name='validate_otp'),
]
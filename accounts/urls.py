from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),   # renamed to avoid conflict
    path("register/", views.register, name="register"),
    path("home/", views.home, name="home"),
    path("logout/", views.user_logout, name="logout"),
    path("verify-email/", views.verify_email, name="verify_email"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),      # OTP verification page
    path("resend-otp/", views.resend_otp, name="resend_otp"),
    path("password/", views.create_password, name="password"),

]

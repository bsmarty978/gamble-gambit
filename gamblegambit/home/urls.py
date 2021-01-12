from django.urls import path
from . import views

urlpatterns =[
    path('',views.homePage,name="home"),
    path('home',views.homePage,name="home"),
    path('login',views.loginPage,name="login"),
    path('logout',views.logoutUserPage,name="logout"),
    path('signup',views.signupPage,name="signup"),
    path('upcoming',views.upcoming,name="upcoming"),
]
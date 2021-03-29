from django.urls import path
from . import views

urlpatterns =[
    path('',views.homePage,name="home"),
    path('home',views.homePage,name="home"),
    path('login',views.loginPage,name="login"),
    path('logout',views.logoutUserPage,name="logout"),
    path('signup',views.signupPage,name="signup"),
    path('myprofile',views.myprofile_page,name="myprofile")
    # path('upcoming',views.upcoming,name="upcoming"), #NOTE: this methid added to create team APP.
]
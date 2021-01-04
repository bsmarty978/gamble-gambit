from django.urls import path
from . import views

urlpatterns =[
    path('<str:title>/',views.create_team,name="create_team"),
    path('sample',views.sample,name="sample"),
]
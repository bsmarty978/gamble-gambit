from django.urls import path
from . import views

urlpatterns =[
    path('<str:title>/',views.create_team,name="create_team"),
    # path('upcoming',views.sample,name="sample"),   #can be used when creating upcmoing match model  inside create matches folder
    path('sample',views.sample,name="sample"),
]
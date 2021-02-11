from django.urls import path
from . import views

urlpatterns =[
    path('<str:title>/',views.create_team,name="create_team"),
    # path('upcoming',views.sample,name="sample"),   #can be used when creating upcmoing match model  inside create matches folder
    path('sample',views.sample,name="sample"),
    path('upcoming',views.upcoming,name="upcoming"),
    path('results',views.completedmatchList,name="completed"),
    path('<str:title>/myteam/',views.confirm_team,name="myteam"),
    path('result/<str:id>',views.match_result_score,name="match_result_score"),
]
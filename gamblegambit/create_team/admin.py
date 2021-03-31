from django.contrib import admin

# Register your models here.
from .models import Matches,MyTeam,UserProfilePage,RsixPlayerList

admin.site.register(Matches)
admin.site.register(MyTeam)
admin.site.register(UserProfilePage)
admin.site.register(RsixPlayerList)

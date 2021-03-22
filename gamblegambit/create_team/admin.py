from django.contrib import admin

# Register your models here.
from .models import Matches,MyTeam,UserProfilePage

admin.site.register(Matches)
admin.site.register(MyTeam)
admin.site.register(UserProfilePage)
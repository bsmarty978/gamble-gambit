from django.contrib import admin

# Register your models here.
from .models import Matches,RsixPlayerList

admin.site.register(Matches)
admin.site.register(RsixPlayerList)
from django.contrib import admin

# Register your models here.
from .models import Matches,MyTeam

admin.site.register(Matches)
admin.site.register(MyTeam)
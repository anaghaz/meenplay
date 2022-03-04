from django.contrib import admin
from projectapp.models import regcoachh
from projectapp.models import venue
from projectapp.models import playerreg
from projectapp.models import payment
from projectapp.models import game
from projectapp.models import time
from projectapp.models import report
from projectapp.models import video
from projectapp.models import msgg
from projectapp.models import admn,team,game_time,team_category

# Register your models here.
admin.site.register(regcoachh)
admin.site.register(venue)
admin.site.register(playerreg)
admin.site.register(payment)
admin.site.register(game)
admin.site.register(time)
admin.site.register(report)
admin.site.register(video)
admin.site.register(msgg)
admin.site.register(admn)
admin.site.register(team)
admin.site.register(game_time)
admin.site.register(team_category)

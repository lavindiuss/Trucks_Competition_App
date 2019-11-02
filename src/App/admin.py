from __future__ import unicode_literals
from django.contrib import admin


from App.models import *


admin.site.register(Competition)
admin.site.register(Trip)
admin.site.register(GpsLog)

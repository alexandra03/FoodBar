from django.db import models
from django.contrib import admin
from person.models import *

admin.site.register(Keyword)
admin.site.register(Profile)
admin.site.register(Preference)

admin.site.register(Restaurant)
admin.site.register(profileRestaurantLink)
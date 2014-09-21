from django.db import models
from django.contrib import admin
from person.models import *

admin.site.register(Keyword)
class Profileadmin(admin.ModelAdmin):
    filter_horizontal = ("keywords",)
admin.site.register(Profile,Profileadmin)
admin.site.register(Preference)

admin.site.register(Restaurant)
admin.site.register(profileRestaurantLink)
admin.site.register(RestaurantDescription)
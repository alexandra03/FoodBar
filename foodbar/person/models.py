from django.db import models
from django.contrib.auth.models import User

class Keyword(models.Model):
	keyword = models.CharField('Keyword', max_length=30)

class Profile(models.Model):
	user = models.ForeignKey(User)
	keywords = models.ManyToManyField(Keyword)

class Preference(models.Model):
	PREF_TYPES = (
		('Ethnicity', 'ethnicity'),
		('Size', 'size'),
		('Atmosphere', 'atmosphere'),
		('Brunch, lunch, dinner, apps?', 'meal_time'),
		('Location', 'location'),
		)
	profiles = models.ForeignKey(Profile)
	name = models.CharField('Preference Name', max_length=256)
	pref_type = models.CharField('Preference Type', choices=PREF_TYPES, max_length=30)
	score = models.IntegerField('Preference Score', default=0)
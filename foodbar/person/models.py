from django.db import models
from django.contrib.auth.models import User

class Keyword(models.Model):
	keyword = models.CharField('Keyword', max_length=30)

	def __unicode__(self):
		return self.keyword

class Profile(models.Model):
	user = models.ForeignKey(User)
	keywords = models.ManyToManyField(Keyword)

	def __unicode__(self):
		return self.user.username

class Preference(models.Model):
	PREF_TYPES = (
		('ethnicity', 'Ethnicity'),
		('size', 'Size'),
		('atmosphere', 'Atmosphere'),
		('meal_time', 'Brunch, lunch, dinner, apps?'),
		('location', 'Location'),
		)
	profiles = models.ForeignKey(Profile)
	name = models.CharField('Preference Name', max_length=256)
	pref_type = models.CharField('Preference Type', choices=PREF_TYPES, max_length=30)
	score = models.IntegerField('Preference Score', default=0)

	def __unicode__(self):
		return 'Name: '+self.name+', Type:'+self.pref_type+', Rating:'+str(self.score)

class Restaurant(models.Model):
	name = models.CharField('Restaurant Name', max_length=100)
	city = models.CharField('City', max_length=100)
	state = models.CharField('State/Province', max_length=100)
	country = models.CharField('Country', max_length=100)
	keywords = models.ManyToManyField(Keyword)

	def __unicode__(self):
		return self.name+', Location: '+self.city+', '+self.state+', '+self.country

class profileRestaurantLink(models.Model):
	profile = models.ForeignKey(Profile)
	restaurant = models.ForeignKey(Restaurant)
	rating = models.IntegerField('Rating Out of 5', default=3)
	comment = models.CharField('Optional Comment', max_length=256)

	def __unicode__(self):
		return self.restaurant.name+' with rating '+str(self.rating)+'/5'

class RestaurantDescription(models.Model):
	PREF_TYPES = (
		('ethnicity', 'Ethnicity'),
		('size', 'Size'),
		('atmosphere', 'Atmosphere'),
		('meal_time', 'Brunch, lunch, dinner, apps?'),
		('location', 'Location'),
		)
	restaurant = models.ForeignKey(Restaurant)
	name = models.CharField('Description Name', choices=PREF_TYPES, max_length=256)
	desc_type = models.CharField('Description Type', max_length=256)		
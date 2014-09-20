from django.contrib.auth.models import User
from person.models import *


class SmartGrouping:
	def __init__(self, user, city='', state='', country=''):
		self.restaurants = Restaurant.objects.filter(city=city, state=state, country=country)
		self.user = user
		self.user_kwds = user.profile_set.all()[0].keywords.all()

	def keyword_group(self):
		'''
		Finds the list of top restaurants that have keywords in common with the user's 
		preference and that they haven't been to (in the given area) 
		'''

		''' First, get the list of restaurants that the user has not been to'''
		res_lst = {}
		for res in self.restaurants:
			if not profileRestaurantLink.objects.filter(profile=user.profile_set.all()[0], restaurant=res).count():
				res_lst.update({res.id: 0})

		''' Attach the number of keywords in common between user/resto, and order '''
		for kw in self.user_kwds:
			matches = self.restaurants.filter(keywords__keyword=kw)
			for match in matches:
				res_lst[match.id]+=1

		''' Remove all restaurants with no matches '''
		matching_res = []
		for res in res_lst:
			if res_lst[res]>0:
				matching_res.append([res,res_lst[res]])

		''' Sort matches, and take top 10 results '''
		sorted_res = sorted(matching_res, key=lambda tup: tup[1])
		sorted_res.reverse()
		sorted_res = sorted_res[:10]
		top_matches = []

		''' Return a list of Restaurant objects '''
		for res in sorted_res:
			top_matches.append(Restaurant.objects.get(pk=res[0]))
		
		return top_matches

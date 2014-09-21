from django.contrib.auth.models import User
from person.models import *


class SmartGrouping:
	def __init__(self, user, city=''):
		self.city=city
		self.restaurants = Restaurant.objects.filter(city=city)
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
			if not profileRestaurantLink.objects.filter(profile=self.user.profile_set.all()[0], restaurant=res).count():
				res_lst.update({res.id: 0})

		''' Attach the number of keywords in common between user/resto, and order '''
		for kw in self.user_kwds:
			matches = self.restaurants.filter(keywords__keyword=kw)
			for match in matches:
				if match.id in res_lst:
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

	def people_group(self):
		'''
		Group people by keywords, list all restaurants they've been to with that keyword, 
		sort the list of restaurants based on the number of people that have been there, get
		rid of the ones that the user has already been to, and show the results with the top 
		ratings given by that group of people
		'''

		''' Start by getting all the people that have rated a restaurant in the desired area '''
		reviews = profileRestaurantLink.objects.filter(
			restaurant__country=self.country, 
			restaurant__state=self.state, 
			restaurant__city=self.city
		)
		profiles = []
		for review in reviews:
			profiles.append(review.profile)

		''' Get rid of all the users that don't have any keywords in common with the main user '''
		matching_profiles = []
		for person in profiles:
			kwds = []
			for kw in person.keywords:
				kwds.append(kw)
			if any(kw in self.user_kwds for kw in kwds):
				matching_profiles.append(person)

		''' Create an undirected edge between the users, such that an edge means a common keyword.
			Note that edges will be duplicated because I'm too lazy to make a data structure that 
			allows for multiple edges between subelements of a node '''
		graph = []
		for kw in self.user_kwds:  # For every keyword
			for profile in matching_profiles:  # Go through all the profiles
				if kw in profile.keywords.all():  # If the profile has the keyword
					for other_profile in matching_profiles:  # Go through all the other profiles
						if other_profile!=profile and kw in other_profile.keywords.all():  # If they have it in common
							graph.append([profile.id, other_profile.id])  # Add the edge to the graph

		''' Find the average number of edges leading to any given node '''
		edge_count = {}
		for profile in matching_profiles:
			edge_count.update({profile.id: 0})

		for edge in graph:
			edge_count.update({edge[0], edge_count[edge[0]]+1})
			edge_count.update({edge[1], edge_count[edge[1]]+1})		

		total_edges = sum(edge[1] for edge in edge_count)
		average_edge_count = float(total_edges)/float(len(edge_count))

		''' If there are enough users, add all the ones that are above a certain threshold of
			clusteriness to the final group of users '''
		user_cluster = []
		if len(edges_count) > 20:
			for node in edge_count:
				if edge_count[node.key()]>(average_edge_count-1):
					user_cluster.append(Profile.objects.get(pk=node.key()))

		''' Get a list of all the restaurants in the area that the cluster of people have rated '''
		clustered_restaurants = []
		for profile_id in user_cluster:
			restaurants = Profile.objects.get(pk=profile_id).profilerestaurantlink_set.filter(
				restaurant__country=self.country, 
				restaurant__state=self.state,
				restaurant__city=self.city
			)
			for restaurant in restaurants:
				clustered_restaurants.append(restaurant)

		''' Make a list of arrays [restaurant, # of occurences] '''
		occ_restos = {}
		for res in clustered_restaurants:
			if res not in occ_restos:
				t = 1
			else:
				t = occ_restos[res]+1
			occ_restos.update({res:t})

		array_restos = []
		for occurence in occ_restos:
			array_restos.append([occurence, occ_restos[occurence]])

		''' Return top 10 restaurants '''			
		sorted_res = sorted(array_restos, key=lambda tup: tup[1])
		sorted_res.reverse()
		return sorted_res[:10]	













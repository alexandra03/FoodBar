from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from person.models import *
from person.suggestions import *

def main(request):
	return render(request, 'main.html', {})

def get_personalized_selection(request):
	if request.method=="GET":
		return render(request, 'base.html', {})
	if request.POST['selection_type']=='all':
		return list_all_businesses(request)
	elif request.POST['selection_type']=='kw':
		return list_keyworded_businesses(request)

def list_all_businesses(request):
	if request.method=="POST":
		restaurants = Restaurant.objects.filter(city=request.POST['location'])
	else:
		restaurants = Restaurant.objects.filter(city='Waterloo')
	return render(request, 'all_businesses.html', {"restaurants":restaurants})

def list_keyworded_businesses(request):
	if request.method=="POST":
		user = User.objects.all()[0]
		groups = SmartGrouping(user, city=request.POST['location'])
		restaurants = groups.keyword_group()
		return render(request, 'all_businesses.html', {'restaurants': restaurants})

def keywords(request):
	user = User.objects.all()[0]
	if request.method=='POST':
		kw = Keyword.objects.get(keyword=request.POST['kw'])
		user.profile_set.all()[0].keywords.add(kw)
	keywords = Profile.objects.get(user=user).keywords.all()
	all_kws = []
	for obj in Keyword.objects.all():
		all_kws.append(str(obj.keyword))
	return render(request, 'keywords.html', {'keywords':keywords, 'autoselect':all_kws})


def restaurant(request, id_number):
	restaurant = Restaurant.objects.get(pk=id_number)
	reviews = profileRestaurantLink.objects.filter(restaurant=restaurant)
	return render(request, 'business.html', {'item':restaurant, 'reviews':reviews})




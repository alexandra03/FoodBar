from person.models import *
from yelp import yelp

def create_restaurants(location):
	from person.models import Keyword, Restaurant
	from yelp import yelp
	yelp = yelp.Yelp()
	num_bus = yelp.count({'location':location, 'term':'food'})
	offset = 0

	while (offset+20)<num_bus:
		businesses = yelp.search({
			'location': location,
			'term':'food',
			'offset':str(offset)
		})
		for bus in businesses:
			if Restaurant.objects.filter(yelp_id=bus['id']).exists():
				continue
			res = Restaurant(
				yelp_id=bus['id'],
				name=bus['name'],
				city=bus['location']['city'],
				state=bus['location']['state_code'],
				country=bus['location']['country_code']
			)
			res.save()
			
			if 'categories' in bus:
				keywords = bus['categories']
			else:
				continue

			for kw in keywords:
				if not Keyword.objects.filter(keyword=kw[0]).exists():
					new_kw = Keyword(keyword=kw[0])
					new_kw.save()
				else:
					new_kw = Keyword.objects.get(keyword=kw[0])
				res.keywords.add(new_kw)

		offset+=20

def add_new_fields(queryset):
	from person.models import Restaurant, Profile
	from yelp import yelp
	yelp = yelp.Yelp()
	for bus in queryset:
		business = yelp.business(bus.yelp_id)
		bus.street = business['location']['address']
		bus.rating = int(business['rating'])
		bus.star_url = business['rating_img_url']
		bus.image_url = business['snippet_image_url']
		bus.save()

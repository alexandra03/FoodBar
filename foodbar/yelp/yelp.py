import requests
from requests_oauthlib import OAuth1

'''
Super simple way to search Yelp API without having to do any
authentication in the code, and without having to construct the 
url. Return list of businesses.

from yelp import yelp
yelp = yelp.Yelp()
yelp.search({'location':'Waterloo Ontario'})

'''

class Yelp:
	def __init__(self):
		self.base_url='http://api.yelp.com/v2/search?'
		self.consumer_key='CoReD2fa2wY_QFyUSw6l5w'
		self.consumer_secret='kRhlJBk5sGesz_r75kKjS42FJv0'
		self.token='8Mb9lCsJis2h02SRBe7a8sTwsc3Fmge3'
		self.token_secret='RdiSAYCG_m0VS1nIK_lMmpLymLE'
		self.auth = OAuth1(self.consumer_key, self.consumer_secret, self.token, self.token_secret)


	def search(self, params, count=False):
		search_url = self.base_url
		for key in params.keys():
			search_url+=key+'='+params[key].replace(' ', '+')+'&'
		response = requests.get(search_url, auth=self.auth)
		if response.status_code != 200:
			raise
		if count:
			return response.json()
		return response.json()['businesses']

	def count(self, params):
		return self.search(params, True)['total']


# Class for interact to PokeAPI
import urllib.request
from urllib.error import HTTPError
import json 

class PokeAPI:

	def __init__(self, url):
		self._url = url
		self._useragent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
		self._headers = {'User-Agent': self._useragent}

	def generate_request(self, query):
		url = self._url + query
		return urllib.request.Request(url, None , self._headers)

	def make_response(self, request):
		try:
			return urllib.request.urlopen(request)
		except HTTPError as error:
			if error.code == 404:
				return -1
			else:
				raise

	def get_data(self, response):
		if response == -1:
			print("Invalid response")
		else:
			return json.load(response)

	def get_image(self, url):
		return urllib.request.urlopen(url).read()


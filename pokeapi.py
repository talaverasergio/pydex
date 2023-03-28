
# Class for interact to PokeAPI
import urllib.request
from urllib.error import HTTPError
import json 
from threading import Thread

class PokeAPI:
	'''
	Used to communicate with the API using urllib requests
	'''

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

	def monitor_thread(self, thread, gui):
		'''
		The gui parameter can be use to invoke the correspondent callback method
		to be called for update the correspondent elements
		'''
		if thread.is_alive():
			gui.root.after(100, lambda: self.monitor_thread(thread,gui))
		else:
			gui.fetch_complete()

class AsyncDownload(Thread):
	'''
	Provides an asynchronous download for to not block the gui main loop
	
	The status property can be used to check the current state of operation
	as follows:
	0 not processed / 1 In progress / 2 Done / -1 Failure
	'''
	def __init__(self, query, api):
			
		super().__init__()

		self.query = query
		self.api = api
		self.response = None
		self.request = self.api.generate_request(self.query)

		
		self.status = 0

	def run(self):
		self.status = 1
		self.response = self.api.make_response(self.request)
		
		if self.response == -1:
			self.status = -1
			self.response = -1
			return 
		else:
			self.status = 2
			return




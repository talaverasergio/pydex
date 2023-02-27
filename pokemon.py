
# Class for representing a Pokemon
class Pokemon:

	def __init__(self):
		self._name = None
		self._pokeid = None
		self._types = None
		self._image_url_front = None
		self._image_path = None

	def __str__(self):
		return "Pokemon: " + str(self._name) + " ID: " + str(self._pokeid) + " Type: " + str(self._types) + " "+ str(self._image_url_front)

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, name):
		self._name = name

	@property
	def pokeid(self):
		return self._pokeid
	@pokeid.setter
	def pokeid(self, pokeid):
		self._pokeid = pokeid

	@property
	def types(self):
		return self._types
	@types.setter
	def types(self, types):
		self._types = types

	@property
	def image_url_front(self):
		return self._image_url_front
	@image_url_front.setter
	def image_url_front(self, url):
		self._image_url_front = url

	@property
	def image_path(self):
		return self._image_path
	@image_path.setter
	def image_path(self, newPath):
		self._image_path = newPath
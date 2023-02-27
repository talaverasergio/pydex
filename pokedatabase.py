
# Class for storing Pokemon() instances in a database
import shelve
import urllib.request
from pokemon import Pokemon

class PokeDatabase:

	def __init__(self):
		self._db = shelve.open('data/db')
		self._db_nameID = {}
		for pokemon in self._db.values():
			self._db_nameID[pokemon.name] = str(pokemon.pokeid)

	def save_data(self, data):

		pokemon = Pokemon()
		pokemon.name = data['name']
		pokemon.pokeid = data['id']
		pokemon.image_url_front = data['sprites']['front_default']
		pokemon.types = [x['type']['name'] for x in data['types']]
		pokemon.image_path = self.save_image(pokemon.image_url_front, pokemon.pokeid)

		self._db_nameID[pokemon.name] = str(pokemon.pokeid)
		self._db[str(pokemon.pokeid)] = pokemon

	def save_image(self, url, pokeid):
		path = 'data/img/' + str(pokeid) + '.png'
		with open(path, 'wb') as f:
			f.write(urllib.request.urlopen(url).read())
		return path

	def check_data(self, query):
		if query.isdecimal():
			return self.search_id(query)
		else:
			try:
				pokeid = self._db_nameID[str(query)]
			except KeyError:
				return None
			else:
				return self.search_id(pokeid)
				
	def search_id(self, pokeid):
		try: 
			pokemon = self._db[str(pokeid)]
		except KeyError:
			return None
		else:
			return pokemon





import shelve
from pokemon import Pokemon

class PokeDatabase:
	'''
	This class is used to store class Pokemon instances into shelve, a python library
	that provides a dictionary-like interface to store persistent data
	'''
	def __init__(self, api):
		self._db = shelve.open('data/db')
		self._db_nameID = {}
		self._api = api
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

		return pokemon

	def save_image(self, url, pokeid):
		path = 'data/img/' + str(pokeid) + '.png'
		with open(path, 'wb') as f:
			f.write(self._api.get_image(url))
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

	def close(self):
		self._db.close()




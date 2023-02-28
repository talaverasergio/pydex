import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import StringVar, ttk
from PIL import ImageTk, Image

from pokedatabase import PokeDatabase
from pokeapi import PokeAPI

class Gui:

	def __init__(self, root, api, db):
		
		self.db = db
		self.api = api
		root.title("PyDex")
		self.icon = ImageTk.PhotoImage(Image.open('assets/icon.png'))
		root.wm_iconphoto(False, self.icon)
		self.splash = ImageTk.PhotoImage(Image.open('assets/splash.png'))
		self.label_splash = tk.Label(image=self.splash)
		self.label_splash.grid(column=1, row=2)

		self.mainframe = ttk.Frame(root)
		self.mainframe.grid(column=0, row=0)

		self.query_input = StringVar()

		self.label_name = ttk.Label(text="Ingrese nombre o ID del Pokémon:")
		self.label_name.grid(column=1,row=1, padx=10, pady=10)

		self.entry_name_id_pokemon = ttk.Entry(width=20, textvariable=self.query_input, takefocus=1)
		self.entry_name_id_pokemon.grid(column=2, row=1)

		self.button_load_query = ttk.Button(text='Buscar', command=self.search_button)
		self.button_load_query.grid(column= 3, row=1, padx=10)

		self.label_pokemon_name = tk.Label(text='-', font=	'Helvetica 14 bold')
		self.label_pokemon_name.grid(column=2, row=3, pady=5)

		self.label_pokemon_type = tk.Label(text='-')
		self.label_pokemon_type.grid(column=2, row=4, pady=5)

		self.label_pokemon_id = tk.Label(text='-')
		self.label_pokemon_id.grid(column=2, row=5, pady=10)

		self.sprite = ImageTk.PhotoImage(Image.open('assets/placeholder.png'))
		self.label_sprite = tk.Label(image=self.sprite)
		self.label_sprite.grid(column=2, row=2)

	def search_button(self):
		query = self.query_input.get().lower()
		pokemon = self.db.check_data(query)

		if query == '':
			return

		if(pokemon is not None):
			self.update_pokemon_info(pokemon)
		else:
			fetched_successfully = False
			
			if self.fetch_pokemon(query) == -1:
				fetched_successfully = False
			else:
				fetched_successfully = True
				self.show_infobox()
				return

			pokemon = self.db.check_data(query)
			
			if fetched_successfully:
				self.update_pokemon_info(pokemon)
			else:
				self.show_infobox()


	def fetch_pokemon(self, query):
		req = self.api.generate_request(query)
		res = self.api.make_response(req)
		if res == -1:
			return False
		else:
			data = self.api.get_data(res)
			self.db.save_data(data)

	def update_pokemon_info(self, pokemon):
		self.label_pokemon_name.configure(text = pokemon.name.capitalize())
		type_string= ""
		for type in pokemon.types:
			type_string = type_string + type.capitalize() + ' '
		self.label_pokemon_type.configure(text= type_string)

		self.label_pokemon_id.configure(text=pokemon.pokeid)

		self.sprite = ImageTk.PhotoImage(Image.open(pokemon.image_path))
		self.label_sprite.configure(image=self.sprite)

	def show_infobox(self):

		tkmsg.showinfo(
			'Pokémon no encontrado', 
			('No se ha encontrado el Pokémon especificado.'
			'Compruebe que el ID o el nombre sea correcto. ' 
			'Tenga en cuenta tambien de poner el nombre completo.'))


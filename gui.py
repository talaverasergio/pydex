import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import StringVar, ttk
from PIL import ImageTk, Image
from pokeapi import AsyncDownload

class Gui:

	def __init__(self, root, api, db):
		
		self.db = db
		self.api = api
		self.root = root
		root.title("PyDex")
		self.icon = ImageTk.PhotoImage(Image.open('assets/icon.png'))
		root.wm_iconphoto(False, self.icon)
		self.splash = ImageTk.PhotoImage(Image.open('assets/splash.png'))
		self.label_splash = tk.Label(image=self.splash)
		self.label_splash.grid(column=1, row=2)

		self.download_thread = None

		self.mainframe = ttk.Frame(root)
		self.mainframe.grid(column=0, row=0)

		self.query_input = StringVar()

		self.label_name = ttk.Label(text="Ingrese nombre o ID del Pokémon:")
		self.label_name.grid(column=1,row=1, padx=10, pady=10)

		self.entry_name_id_pokemon = ttk.Entry(width=20, textvariable=self.query_input, takefocus=1)
		self.entry_name_id_pokemon.grid(column=2, row=1)
		self.entry_name_id_pokemon.bind('<Return>', lambda e: self.search_button())

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
		
		if query == '':
			return
	
		self.button_load_query.configure(text='Buscando...')
		self.button_load_query.configure(state=tk.DISABLED)
		self.entry_name_id_pokemon.configure(state=tk.DISABLED)
		pokemon = self.db.check_data(query)
	
		if(pokemon is not None):
			self.update_pokemon_info(pokemon)
			self.button_load_query.configure(text='Buscar')
			self.button_load_query.configure(state=tk.NORMAL)
			self.entry_name_id_pokemon.configure(state=tk.NORMAL)
		else:
			self.fetch_pokemon(query)
			
	def fetch_pokemon(self, query):
		self.download_thread = AsyncDownload(query,self.api)
		self.download_thread.start()
		self.api.monitor_thread(self.download_thread, self)

	def fetch_complete(self):
		self.button_load_query.configure(text='Buscar')
		self.button_load_query.configure(state=tk.NORMAL)
		self.entry_name_id_pokemon.configure(state=tk.NORMAL)
		
		if self.download_thread.status == -1:
			self.show_infobox()

		if self.download_thread.status == 2:
			pokemon = self.db.save_data(self.api.get_data(self.download_thread.response))
			self.update_pokemon_info(pokemon)

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
			('No se ha encontrado el Pokémon especificado. '
			'Compruebe que el ID o el nombre sea correcto. ' 
			'Tenga en cuenta tambien de poner el nombre completo.'))


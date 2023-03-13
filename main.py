
import tkinter as tk
from pokeapi import PokeAPI
from pokedatabase import PokeDatabase
from gui import Gui

API_URL: str = 'https://pokeapi.co/api/v2/pokemon/'

if __name__ == '__main__':
	api = PokeAPI(API_URL)
	db = PokeDatabase(api)
	root = tk.Tk()
	app = Gui(root, api, db)
	root.mainloop()
	db.close()
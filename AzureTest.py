import tkinter
import tkinter.ttk as ttk	# Tkinter styles
from tkintermapview import TkinterMapView

class App(tkinter.Tk):
	def __init__(self):
		super(App, self).__init__()
		self.title("Styling test")
		self.geometry('800x400')
		self.load_theme()
		self.build_widgets()

	def load_theme(self):
		style = ttk.Style(self)        								# Window to which we want to apply the style
		self.tk.call('source', 'azure dark/azure dark.tcl')			# Load theme library
		style.theme_use('azure')

		style.configure('Accentbutton', foreground='white')
		style.configure('Togglebutton', foreground='white')
		style.configure('Switch', foreground='white')
		# self.configure(bg='lightblue')  --> This can be used to change bg color

	def build_widgets(self):
		fr = tkinter.Frame(self)
		fr.grid(column=0, row=0, padx=10, pady=10)

		button1 = ttk.Button(self, text='Prueba', style='Accentbutton')
		button1.grid(column=1, row=2, pady=15, columnspan=2, sticky='we')										# Do not use col=0 & row=0, or it will overwrite frame grid

		state = tkinter.IntVar()
		self.switch = ttk.Checkbutton(self, text='Switch' ,style='Switch', variable=state, onvalue=1, offvalue=0)
		self.switch.grid(column=1, row=3, pady=15, sticky='we')						# Padx applies only to this widget, but padx applies to all in same column
		self.switch.config(command=lambda: self.switch_function(state))

		#MENUBUTTON
		selected = tkinter.StringVar()
		selected.set("Menu")
		menu = tkinter.Menu(self, tearoff=False)						    # Tearoff true allows to cut options in another window, false does opposite
		menu.add_radiobutton(label='Option1', variable=selected, value='Option1', command= lambda: self.displayVar(selected))
		menu.add_separator()       # RadioButton are buttons that display menu options and can save a selected value with variable=
								   # Lambdas are used to pass arguments to methods without creating global or self variables
								   # Command= is called whenever an option in the menu is pressed
		menu.add_radiobutton(label='Option2', variable=selected, value='Option2', command= lambda: self.displayVar(selected))
		menuButton = ttk.Menubutton(self, textvariable=selected, menu=menu, direction='below')
		menuButton.grid(column=1, row=4, pady=15, sticky='we')

		'''
		#SCROLLBAR
		scrollbar = ttk.Scrollbar(self)
		scrollbar.grid(column=0, row=1, sticky='N')
		'''

		#MAP VIEW
		map_widget = TkinterMapView(self, width=400, height=300)
		map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=50)
		map_widget.set_address("Colima Mexico", marker=True)
		map_widget.grid(column=3, row=1, rowspan=4, padx=30, pady=15, sticky='n')


	def displayVar(self, variable: tkinter.StringVar):
		print(variable.get())

	def switch_function(self, state):
		if state.get():
			self.switch.config(text='On')
		else:
			self.switch.config(text='Off')

if __name__ == '__main__':
	try:
		gui = App()
		gui.mainloop()
	except KeyboardInterrupt:
		exit()
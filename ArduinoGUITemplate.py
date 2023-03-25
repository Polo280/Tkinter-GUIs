import tkinter
import customtkinter
import serial

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super(App, self).__init__()
        self.geometry('780x520')
        self.title('CANSAT TEST')
        self.arduino = serial.Serial()
        self.connected = False

        # Frame Left
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=18)
        self.frameLeft = customtkinter.CTkFrame(self, width=200, corner_radius=5)   # El frame es un contenedor recatangular
        self.frameLeft.grid(row=0, column=0, sticky='nswe', padx=10, pady=10)       # nwse hace que se alargue en todas direcciones

        # Frame Right
        self.frameRight = customtkinter.CTkFrame(self, width=580)
        self.frameRight.grid(row=0, column=1, padx=10, pady=20, sticky='nswe')

        # Call layouts
        self.layouts()
        self.build_widgets()

    def layouts(self):
        # Layout Left
        self.frameLeft.rowconfigure(0, minsize=20)
        self.frameLeft.rowconfigure(2, minsize=10)
        self.frameLeft.rowconfigure(4, minsize=10)
        self.frameLeft.rowconfigure(6, minsize=15)

        # Layout right
        self.frameRight.rowconfigure(0, minsize=30)       # More accurate alternative for padx/pady
        self.frameRight.columnconfigure(0, minsize=30)

    def build_widgets(self):
        # Communication label
        self.label1 = customtkinter.CTkLabel(master=self.frameLeft, text='COMUNICACION', text_font=('Trebuchet Ms', -17))
        self.label1.grid(row=1, column=0, padx=10, pady=10)

        # Combobox (option menu)
        self.baud_rates = customtkinter.CTkComboBox(master=self.frameLeft, values=['9600', '2400', '4800', '9600',
                                                                '14400', '19200', '28800', '38400', '57600', '115200'])
        self.baud_rates.grid(row=3, column=0, padx=10)

        # Combobox (COM ports)
        self.ports = customtkinter.CTkComboBox(master=self.frameLeft, values=['COM5', 'COM7', 'COM13'])
        self.ports.grid(row=5, column=0, padx=10)

        # Connection Button
        connection_state = tkinter.StringVar()
        connection_state.set('Connect')
        self.connect_button = customtkinter.CTkButton(master=self.frameLeft, text_font=('Trebuchet Ms', -17),
                              textvariable=connection_state, command=self.connect_press, borderwidth=2)  # Command without ()
        self.connect_button.grid(row=7, column=0, padx=10)

        # ---RIGHT LAYOUT---
        # Label (title)
        self.titleRight = customtkinter.CTkLabel(master=self.frameRight, text='ARDUINO DATA', text_font=('Trebuchet Ms', 15))
        self.titleRight.grid(row=1, column=1)

    def connect_press(self):
        port = self.ports.get()
        rate = self.baud_rates.get()
        state = tkinter.StringVar()
        if not self.connected:
            try:
                self.arduino.__init__(port=port, baudrate=rate, bytesize=serial.EIGHTBITS, timeout=None)
                state.set("Disconnect")
                self.connect_button.configure(textvariable=state)
                self.connected = True
            except Exception as ex:
                print(ex)
        else:
            state.set("Connect")
            self.connect_button.configure(textvariable=state)
            self.arduino.close()
            self.connected = False


if __name__ == '__main__':
    try:
        app = App()
        app.mainloop()
    except KeyboardInterrupt:
        exit()
import threading
import serial
import time
import tkinter
import tkintermapview
import customtkinter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from math import floor


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super(App, self).__init__()
        self.start_time = 0
        self.geometry('1500x720')
        self.title('CANSAT TEST')

        # Arduino read
        self.arduino = serial.Serial()
        self.updateThread = threading.Thread()
        self.connected = False
        self.runArduino = threading.Event()
        self.data = []

        # Frame Left
        #self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0)
        self.frameLeft = customtkinter.CTkFrame(self, width=200,
                                                corner_radius=5)  # El frame es un contenedor recatangular
        self.frameLeft.grid(row=0, column=0, sticky='nswe', padx=10,
                            pady=10)  # nwse hace que se alargue en todas direcciones
        self.map = tkintermapview.TkinterMapView()

        # Frame Right
        #self.grid_columnconfigure(1, weight=1)
        self.frameRight = customtkinter.CTkFrame(self, width=700)
        self.frameRight.grid(row=0, column=1, pady=10, sticky='nsw')

        # Frame right 2
        self.grid_columnconfigure(2, weight=5)
        self.frameRight2 = customtkinter.CTkFrame(self, width=400)
        self.frameRight2.grid(row=0, column=2, sticky='nswe', pady=10, padx=10)

        # Call layouts
        self.layouts()
        self.build_widgets()

    def layouts(self):
        # Layout Left
        self.frameLeft.rowconfigure(0, minsize=20)
        self.frameLeft.rowconfigure(2, minsize=10)
        self.frameLeft.rowconfigure(4, minsize=10)
        self.frameLeft.rowconfigure(6, minsize=15)
        self.frameLeft.rowconfigure(8, minsize=60)
        self.frameLeft.rowconfigure(10, minsize=15)
        self.frameLeft.rowconfigure(12, minsize=35)

        # Layout right
        self.frameRight.rowconfigure(0, minsize=30)
        self.frameRight.rowconfigure(2, minsize=30)
        self.frameRight.rowconfigure(4, minsize=40)
        self.frameRight.rowconfigure(6, minsize=50)
        self.frameRight.columnconfigure(0, minsize=15)  # Minsize specified for all columns
        self.frameRight.columnconfigure(1, weight=1)    # Width 1 is to separate evenly all the columns with content
        self.frameRight.columnconfigure(2, weight=1)    # Given both parameters, the library calculates automatically
        self.frameRight.columnconfigure(3, weight=1)

        # Layout right 2
        self.frameRight2.rowconfigure(0, minsize=30)
        self.frameRight2.columnconfigure(0, minsize=15)


    def build_widgets(self):
        # ---LEFT LAYOUT---
        # Communication label
        self.label1 = customtkinter.CTkLabel(master=self.frameLeft, text='COMMUNICATION',
                                             text_font=('Trebuchet Ms', -17))
        self.label1.grid(row=1, column=0, padx=10, pady=10)

        # Combobox (option menu)
        self.baud_rates = customtkinter.CTkComboBox(master=self.frameLeft, values=['9600', '2400', '4800', '9600',
                                                                                   '14400', '19200', '28800', '38400',
                                                                                   '57600', '115200'])
        self.baud_rates.grid(row=3, column=0, padx=10)

        # Combobox (COM ports)
        self.ports = customtkinter.CTkComboBox(master=self.frameLeft, values=['COM5', 'COM7', 'COM13'])
        self.ports.grid(row=5, column=0, padx=10)

        # Connection Button
        connection_state = tkinter.StringVar()
        connection_state.set('Connect')
        self.connect_button = customtkinter.CTkButton(master=self.frameLeft, text_font=('Trebuchet Ms', -17),
                                                      textvariable=connection_state, command=self.connect_press,
                                                      borderwidth=2)  # Command without ()
        self.connect_button.grid(row=7, column=0, padx=10)

        # Label map themes
        self.labelMapTheme = customtkinter.CTkLabel(master=self.frameLeft, text_font=('Trebuchet Ms', -17), text='Map servers')
        self.labelMapTheme.grid(row=9, column=0, padx=10)

        # Combobox (map theme)
        self.mapThemes = customtkinter.CTkComboBox(self.frameLeft, values=['Open Street', 'Google', 'Satellite'],
                                                   command=self.set_server)   # Command automatically passes choice in str type
        self.mapThemes.grid(row=11, column=0, padx=10)

        self.current_plots = 1
        self.change_plot = customtkinter.CTkButton(self.frameLeft, text_font=('Trebuchet Ms', -17), text='Change plots'
                                                   ,command=self.show_plots)
        self.change_plot.grid(row=13, column=0, padx=10)

        # ---RIGHT LAYOUT---
        # Label (title)
        self.titleRight = customtkinter.CTkLabel(master=self.frameRight, text='ARDUINO DATA',
                                                 text_font=('Verdana', 17), text_color='white')
        self.titleRight.grid(row=1, columnspan=9, sticky='n')

        # Temperature labels
        self.temperature = tkinter.StringVar()
        self.temperature.set('NA')
        self.tempLabel = customtkinter.CTkLabel(master=self.frameRight, text_font=('Trebuchet Ms', -19),
                                                text='Temperature')
        self.tempLabel.grid(row=3, column=0, padx=15)
        self.tempvalLabel = customtkinter.CTkLabel(master=self.frameRight, text_font=('Trebuchet Ms', -19),
                                                   textvariable=self.temperature, fg_color='gray')
        self.tempvalLabel.grid(row=3, column=1)

        # Humidity
        self.humidity = tkinter.StringVar()
        self.humidity.set('NA')
        self.humLabel = customtkinter.CTkLabel(master=self.frameRight, text_font=('Trebuchet Ms', -19),
                                               text='Humidity')
        self.humLabel.grid(row=3, column=2)
        self.humvalLabel = customtkinter.CTkLabel(master=self.frameRight, text_font=('Trebuchet Ms', -19),
                                                  textvariable=self.humidity, fg_color='darkblue')
        self.humvalLabel.grid(row=3, column=3, padx=15)

        # Ozone value
        self.o3 = tkinter.StringVar()
        self.o3.set('NA')
        self.ozoneLabel = customtkinter.CTkLabel(master=self.frameRight, text_font=('Trebuchet Ms', -19), text='Ozone')
        self.ozoneLabel.grid(row=5, column=0, padx=15)
        self.ozonevalLabel = customtkinter.CTkLabel(master=self.frameRight, text_font=('Trebuchet Ms', -19),
                                                    textvariable=self.o3, fg_color='gray')
        self.ozonevalLabel.grid(row=5, column=1, padx=15)

        # Altitude
        self.altitude = tkinter.StringVar()
        self.altitude.set('0.0 m')
        self.altitudeLabel = customtkinter.CTkLabel(master=self.frameRight, text_font=('Trebuchet Ms', -19), text='Altitude')
        self.altitudeLabel.grid(row=5, column=2, padx=15)
        self.altitudevalLabel = customtkinter.CTkLabel(master=self.frameRight, text_font=('Trebuchet Ms', -19),
                                                    textvariable=self.altitude, fg_color='gray')
        self.altitudevalLabel.grid(row=5, column=3, padx=15)

        # Map view
        self.map.__init__(self.frameRight, corner_radius=5, width=650, height=550)
        self.map.set_address('Guadalajara Jalisco')
        self.marker = self.map.set_marker(48.8534000, 2.3486000, text="Cansat")
        self.map.set_zoom(15)
        self.map.grid(row=7, columnspan=9, pady=20)

        # ---RIGHT 2 FRAME---
        self.right2Title = customtkinter.CTkLabel(self.frameRight2, text_font=('Verdana', 15), text='REAL TIME PLOTS', text_color='white')
        self.right2Title.grid(row=0, column=0, padx=20, pady=20)

        # MATPLOT LIB
        self.ozone_data = [0.00] * 50    # Data lists to plot, fill them with zeroes to init plotting since program starts
        self.humidity_data = [0.0] * 50
        self.current_time = [0.0] * 50

        self.figure = plt.figure(figsize=[6, 6])  # Create figure to add plot there
        self.plot_canvas = FigureCanvasTkAgg(self.figure, self.frameRight2)
        self.plot_canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=20)        # Convert plot canvas to tkinter widget
        self.start_time = time.time()

        plt.subplot(2, 1, 1)
        plt.title('MQ-131')
        plt.ylabel('Ozone PPM')
        plt.xlabel('Time')

        plt.subplot(2, 1, 2)
        plt.tight_layout(h_pad=1, w_pad=1)
        plt.ylabel('Humidity %')
        plt.xlabel('Time')

        self.temperature_data = [0.0] * 50
        self.figure2 = plt.figure(figsize=[6, 6])
        plt.subplot(2, 1, 1)
        plt.title('Tempereture')
        plt.ylabel('Temp °C')
        plt.xlabel('Time')

        self.ani = animation.FuncAnimation(self.figure, self.animate, fargs=(self.current_time, self.ozone_data,
                                                                        self.humidity_data), interval=10000)  # Use interval for delay, DONT USE SLEEP
        #self.ani2 = animation.FuncAnimation(self.figure2, self.animate2, fargs=(self.current_time, self.temperature_data), interval=10000)

    def set_server(self, server: str):  # Method to choose map server display based on combobox choice
        if server == "Open Street":
            self.map.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif server == "Google":
            self.map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif server == "Satellite":
            self.map.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def connect_press(self):
        port = self.ports.get()
        rate = self.baud_rates.get()
        state = tkinter.StringVar()
        if not self.connected:
            try:
                self.arduino.__init__(port=port, baudrate=rate, bytesize=serial.EIGHTBITS, timeout=0.5)
                state.set("Disconnect")
                self.connected = True                               # Fo read thread management
                self.connect_button.configure(textvariable=state)
                self.updateThread.__init__(target=self.read_data)   # Configure and start thread for reading data from arduino
                self.updateThread.start()
            except Exception as ex:
                print(ex)
        else:
            state.set("Connect")
            self.connect_button.configure(textvariable=state)
            self.arduino.close()
            self.connected = False

    def read_data(self):    # Syntax: [hum, temp, lat, lon, alt, o3]
        if self.connected:
            self.runArduino.set()   # Set to true
        else:
            self.runArduino.clear()  # Set to false

        while True:
            self.runArduino.wait()  # Do not read until arduino is connected
            try:
                self.arduino.write('Data'.encode('ascii'))
                msg = self.arduino.readline().decode('ascii').removesuffix('\r\n')
                data = msg.split(',')
                self.data = data
                if len(data) > 1:
                    self.updateData(data)
                    print(data)
            except:
                pass
            time.sleep(5)

    def updateData(self, data: list):
        if self.connected:
            lng = float(data[2])
            lat = float(data[3])
            self.altitude.set(data[4] + ' m')
            self.o3.set(data[5] + ' PPM')
            if data[0] != ' NAN':
                try:
                    self.humidity.set(data[0] + ' %')
                    self.temperature.set(data[1] + ' °C')
                except Exception as ex:
                    print(ex)

            if lat != 0 and lng != 0:
                try:
                    self.marker.set_position(lat, lng)
                except Exception as ex:
                    print(ex)
        else:
            time.sleep(1)

    def show_plots(self):
        if self.current_plots == 1:
            self.plot_canvas.get_tk_widget().destroy()
            self.plot_canvas = FigureCanvasTkAgg(self.figure, self.frameRight2)
            self.plot_canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=20)
        elif self.current_plots == 2:
            self.plot_canvas.get_tk_widget().destroy()
            self.plot_canvas = FigureCanvasTkAgg(self.figure2, self.frameRight2)
            self.plot_canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=20)


    def animate(self, i, current_time: [], ozone_data: [], humidity_data: []):   # This function is to plot data in real time
        try:
            current = floor(time.time() - self.start_time)

            current_time.append(current)  # Appending has to be done before limiting list size, or it wont append correctly
            ozone_data.append(self.data[5])
            if self.humidity.get() == 'NA':     # Error control to prevent NAN data
                humidity_data.append(50)
            else:
                humidity_data.append(float(self.humidity.get().removesuffix(' %')))


            current_time = current_time[-50:]   # Limit number of elements in lists
            ozone_data = ozone_data[-50:]
            humidity_data = humidity_data[-50:]

            plt.subplot(2, 1, 1)    # Configure first subplot
            plt.cla()               # Clears all data, including labels and titles
            plt.title('MQ-131')
            plt.ylabel('Ozone PPM')
            plt.xlabel('Time')
            plt.plot(current_time, ozone_data)

            plt.subplot(2, 1, 2)  # Configure first subplot
            plt.cla()  # Clears all data, including labels and titles
            plt.ylabel('Hum %')
            plt.xlabel('Time')
            # plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.plot(current_time, humidity_data)

        except Exception as ex:
            print(ex)

    def animate2(self, i, temperature_data: [], current_time: []):
        current = floor(time.time() - self.start_time)

        current_time.append(current)
        current_time = current_time[-50:]


if __name__ == '__main__':
    try:
        app = App()
        app.mainloop()
    except Exception as ex:
        print(ex)
        exit()

import serial
import tkinter as tk
from tkinter import ttk
import threading
import time

# Configure the serial connection (adjust the port accordingly)
arduino = serial.Serial(port='COM10', baudrate=9600, timeout=1)

# Function to toggle LED or Fan
def toggle_device(device):
    if device == '1':
        arduino.write(b'1')  # Toggle LED
    elif device == '2':
        arduino.write(b'2')  # Toggle Fan

# Function to read temperature and humidity from the Arduino
def read_sensor_data():
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            sensor_data_text.insert(tk.END, line + "\n")
            sensor_data_text.see(tk.END)  # Auto-scroll to the latest entry
        time.sleep(2)

# Function to start a background thread for reading sensor data
def start_reading_thread():
    threading.Thread(target=read_sensor_data, daemon=True).start()

# Function for toggling LED via button press
def toggle_led():
    toggle_device('1')

# Function for toggling Fan via button press
def toggle_fan():
    toggle_device('2')

# Create the main window
root = tk.Tk()
root.title("Arduino Control Panel")
root.geometry("500x400")  # Adjust window size

# Apply modern theme and font styling
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 14))
style.configure("TFrame", padding=20)

# Create a frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

# Create the LED toggle button
led_button = ttk.Button(button_frame, text="Toggle LED", command=toggle_led)
led_button.grid(row=0, column=0, padx=20)

# Create the Fan toggle button
fan_button = ttk.Button(button_frame, text="Toggle Fan", command=toggle_fan)
fan_button.grid(row=0, column=1, padx=20)

# Create a frame for sensor data display
sensor_frame = ttk.Frame(root)
sensor_frame.pack(pady=10)

# Add a label for the sensor data
sensor_label = ttk.Label(sensor_frame, text="Temperature and Humidity Data:")
sensor_label.pack(anchor="w")

# Create a text box for displaying sensor data
sensor_data_text = tk.Text(sensor_frame, width=50, height=10, wrap="word", font=("Courier New", 10))
sensor_data_text.pack(pady=10)

# Add a scroll bar for the sensor data text box
scrollbar = ttk.Scrollbar(sensor_frame, command=sensor_data_text.yview)
sensor_data_text.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Start reading sensor data in a background thread
start_reading_thread()

# Start the Tkinter event loop
root.mainloop()

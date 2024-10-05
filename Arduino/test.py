import serial
import streamlit as st
import threading
import time

# Serial initialization (will be opened later)
arduino = None

# Function to open the serial connection
def open_serial_connection():
    global arduino
    if arduino is None or not arduino.is_open:
        try:
            arduino = serial.Serial(port='COM10', baudrate=9600, timeout=1)
            st.success("Serial port opened successfully!")
        except serial.SerialException as e:
            st.error(f"Failed to open serial port: {e}")

# Function to toggle LED or Fan
def toggle_device(device):
    open_serial_connection()  # Ensure the connection is open before sending commands
    if arduino and arduino.is_open:
        if device == '1':
            arduino.write(b'1')  # Toggle LED
        elif device == '2':
            arduino.write(b'2')  # Toggle Fan

# Function to read temperature and humidity from the Arduino
def read_sensor_data():
    open_serial_connection()  # Ensure the connection is open for reading
    while True:
        if arduino and arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            sensor_data_display.text_area("Temperature and Humidity Data", line, height=200)
        time.sleep(2)

# Streamlit app layout
st.title("Arduino Control Panel")

# Buttons to toggle LED and Fan
col1, col2 = st.columns(2)

with col1:
    if st.button("Toggle LED"):
        toggle_device('1')

with col2:
    if st.button("Toggle Fan"):
        toggle_device('2')

# Placeholder for displaying sensor data
sensor_data_display = st.empty()

# Start the background thread to read sensor data (if not already running)
if 'thread_started' not in st.session_state:
    st.session_state.thread_started = True
    threading.Thread(target=read_sensor_data, daemon=True).start()

# Ensure serial port is closed when the app is done
if arduino and arduino.is_open:
    arduino.close()
import serial
import tkinter as tk
from tkinter import ttk
import threading
import time
import pickle

# Load the trained models
with open('fan_model.pkl', 'rb') as f:
    fan_model = pickle.load(f)

with open('light_model.pkl', 'rb') as f:
    light_model = pickle.load(f)

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
            
            # Extract temperature and humidity from line
            # Example: assume the data is formatted as "temp:25 humidity:50"
            try:
                temp_str, humidity_str = line.split(' ')
                temp = float(temp_str.split(':')[1])
                humidity = float(humidity_str.split(':')[1])
                
                # Use the AI model to predict fan and light status
                control_devices(temp, humidity)
            except:
                pass
        time.sleep(2)

# Function to control devices using AI model
def control_devices(temp, humidity):
    # Use models to predict device status
    prediction_fan = fan_model.predict([[temp, humidity]])[0]
    prediction_light = light_model.predict([[temp, humidity]])[0]

    # Control Fan
    if prediction_fan == 1:
        toggle_device('2')  # Turn on fan
    else:
        toggle_device('2')  # Turn off fan

    # Control Light
    if prediction_light == 1:
        toggle_device('1')  # Turn on light
    else:
        toggle_device('1')  # Turn off light

# Start reading sensor data in a background thread
def start_reading_thread():
    threading.Thread(target=read_sensor_data, daemon=True).start()

# Create the main window
root = tk.Tk()
root.title("AI-Controlled Arduino Panel")
root.geometry("500x400")

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

# Start the reading thread
start_reading_thread()

# Start the Tkinter event loop
root.mainloop()

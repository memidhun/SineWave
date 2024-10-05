import streamlit as st

# Sentinel Home Page
st.title("Sentinel")
st.subheader('"An Intelligent Caretaker for Your Sweet Home"')

# Sidebar for navigation
st.sidebar.title("Navigate")
page = st.sidebar.radio("Go to", ["Room Controls", "Surveillance System", "Pet Care", "Chatbot"])

if page == "Room Controls":
    st.write("Welcome to Sentinel ! Your intelligent all-in-one home monitoring and control system.")
    
    # Display four tiles for Lights, Fans, Windows, and Cleaning Robots control in 4 rooms
    st.write("### Room Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("light_icon.png", width=50)
        st.write("#### Lights Control")
        room_lights = st.selectbox("Select Room for Lights", ["Room 1", "Room 2", "Room 3", "Room 4"], key="lights")
        if st.button(f"Toggle Lights in {room_lights}", key="lights_button"):
            st.write(f"Lights toggled in {room_lights}.")
    
    with col2:
        st.image("fan_icon.png", width=50)
        st.write("#### Fan Control")
        room_fans = st.selectbox("Select Room for Fan", ["Room 1", "Room 2", "Room 3", "Room 4"], key="fans")
        if st.button(f"Toggle Fan in {room_fans}", key="fans_button"):
            st.write(f"Fan toggled in {room_fans}.")
    
    col3, col4 = st.columns(2)
    with col3:
        st.image("window_icon.png", width=50)
        st.write("#### Window Control")
        room_windows = st.selectbox("Select Room for Windows", ["Room 1", "Room 2", "Room 3", "Room 4"], key="windows")
        if st.button(f"Toggle Window in {room_windows}", key="windows_button"):
            st.write(f"Window status changed in {room_windows}.")
    
    with col4:
        st.image("robot_icon.png", width=50)
        st.write("#### Cleaning Robots")
        if st.button("Deploy Cleaning Robot", key="robot_button"):
            st.write("Cleaning robot deployed in all rooms.")
    
elif page == "Surveillance System":
    st.subheader("Surveillance System")
    st.write("View your home’s live surveillance feed and gas sensor status.")
    
    # Live feed placeholder (you can embed a camera feed here)
    st.image("live_feed_placeholder.jpg", caption="Live Feed")
    
    # Gas Sensor Data
    gas_levels = st.slider("Gas Sensor Levels", 0, 100)
    if gas_levels > 70:
        st.error("Dangerous gas levels detected!")
    
    # Intruder Alert
    st.write("#### Intruder Alert System")
    intruder_status = st.radio("Intruder Status", ["Safe", "Alert"])
    if intruder_status == "Alert":
        st.warning("Intruder detected! Taking actions...")
    
elif page == "Pet Care":
    st.subheader("Automatic Pet Care System")
    
    # Dispense food and water
    if st.button("Dispense Food"):
        st.write("Dispensing food to your pet...")
        
    if st.button("Dispense Water"):
        st.write("Dispensing water to your pet...")
    
    # Live feed from pet camera
    st.image("pet_camera_placeholder.jpg", caption="Pet Camera Feed")

elif page == "Chatbot":
    st.subheader("Smart Home Chatbot")
    st.write("Ask about your home status or perform actions through the chatbot.")
    
    user_input = st.text_input("You: ", "")
    if st.button("Send"):
        st.write(f"Chatbot: Responding to '{user_input}'...")



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

# Create a frame for buttons
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Create the LED toggle button
led_button = ttk.Button(button_frame, text="Toggle LED", command=toggle_led)
led_button.grid(row=0, column=0, padx=10, pady=10)

# Create the Fan toggle button
fan_button = ttk.Button(button_frame, text="Toggle Fan", command=toggle_fan)
fan_button.grid(row=0, column=1, padx=10, pady=10)

# Create a frame for sensor data display
sensor_frame = ttk.Frame(root, padding="10")
sensor_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

# Add a label for the sensor data
sensor_label = ttk.Label(sensor_frame, text="Temperature and Humidity Data:")
sensor_label.grid(row=0, column=0, sticky=tk.W)

# Create a text box for displaying sensor data
sensor_data_text = tk.Text(sensor_frame, width=50, height=10, wrap="word")
sensor_data_text.grid(row=1, column=0, pady=10)

# Start reading sensor data in a background thread
start_reading_thread()

# Start the Tkinter event loop
root.mainloop()
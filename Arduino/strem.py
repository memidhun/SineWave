import serial
import streamlit as st
import threading
import time

# Configure the serial connection (adjust the port accordingly)
arduino = serial.Serial(port='COM10', baudrate=9600, timeout=1)

# Placeholder for displaying sensor data
sensor_data_display = st.empty()

# Streamlit doesn't support continuous background threading directly, so we need a workaround
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

# Start the background thread to read sensor data
if 'thread_started' not in st.session_state:
    st.session_state.thread_started = True
    threading.Thread(target=read_sensor_data, daemon=True).start()

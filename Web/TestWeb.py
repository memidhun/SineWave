import streamlit as st
import pandas as pd
import cv2
import datetime
from keras.models import load_model
import numpy as np
import time
import os
import random
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
# Backend: Simulate automatic data fetching (replace with real IoT device data fetching logic)
def fetch_device_status():
    # Simulated CSV data as a pandas DataFrame (replace with actual data source)
    data = {
        "Room": ["Room 1", "Room 2", "Room 3", "Room 4"],
        "Lights": ["On", "Off", "On", "Off"],
        "Fans": ["Off", "Off", "On", "On"],
        "Windows": ["Closed", "Open", "Closed", "Closed"],
        "CleaningRobot": ["Idle", "Active", "Idle", "Active"]
    }
    return pd.DataFrame(data)

# Initialize session state to store user-made changes
if "manual_changes" not in st.session_state:
    st.session_state.manual_changes = {}

# Function to apply manual changes and persist them across modes
def apply_manual_changes(device, room, new_status):
    st.session_state.manual_changes[(device, room)] = new_status

# Fetch current device status (automatic from backend)
device_status_df = fetch_device_status()

# Update the device status DataFrame with any manual changes
for (device, room), new_status in st.session_state.manual_changes.items():
    device_status_df.loc[device_status_df['Room'] == room, device] = new_status

# Sentinel Home Page
st.title("Sentinel")
st.subheader('"An Intelligent Caretaker for Your Sweet Home"')

# Sidebar for navigation
st.sidebar.title("Navigate")
page = st.sidebar.radio("Go to", ["Home", "Surveillance System", "Pet Care System", "Chatbot"])

# Main page: Automatic/Manual mode toggle switch
st.write("### Control Mode")
mode = st.toggle("Manual Mode", key="control_mode")
mode_name = "Manual" if mode else "Automatic"
st.write(f"Current Mode: **{mode_name}**")
def control_device(command):
    command = command.lower()
    rooms = ["room 1", "room 2", "room 3", "room 4"]
    devices = {"lights": "Lights", "fans": "Fans", "windows": "Windows", "cleaning robot": "CleaningRobot"}

    for room in rooms:
        if room in command:
            for device, device_key in devices.items():
                if device in command:
                    new_status = "on" if "on" in command else "off" if "off" in command else None
                    if new_status:
                        apply_manual_changes(device_key, room.capitalize(), "On" if new_status == "on" else "Off")
                        return f"{device.capitalize()} in {room.capitalize()} turned {new_status}."
                    else:
                        return f"Specify 'on' or 'off' to control the {device} in {room.capitalize()}."
    return "Sorry, I couldn't understand the command. Please specify the device and the room."

if page == "Home":
    st.write("Welcome to Sentinel! Your intelligent all-in-one home monitoring and control system.")
    
    # Display four tiles for Lights, Fans, Windows, and Cleaning Robots control in 4 rooms
    st.write(f"### Smart Device Control for 4 Rooms - Mode: {mode_name}")

    col1, col2 = st.columns(2)
    with col1:
        st.image("light_icon.png", width=50)  # Original icon size
        st.write("#### Lights Control")
        room_lights = st.selectbox("Select Room for Lights", ["Room 1", "Room 2", "Room 3", "Room 4"], key="lights")
        light_status = device_status_df.loc[device_status_df['Room'] == room_lights, 'Lights'].values[0]
        
        if mode:
            if st.button(f"Toggle Lights in {room_lights}", key="lights_button"):
                new_status = "Off" if light_status == "On" else "On"
                apply_manual_changes("Lights", room_lights, new_status)
                light_status = new_status
                st.write(f"Lights toggled in {room_lights}.")
        
        # Status bubble
        st.markdown(f"**Current Light Status:** {'🟢' if light_status == 'On' else '🔴'} {light_status}")

    with col2:
        st.image("fan_icon.png", width=50)  # Original icon size
        st.write("#### Fan Control")
        room_fans = st.selectbox("Select Room for Fan", ["Room 1", "Room 2", "Room 3", "Room 4"], key="fans")
        fan_status = device_status_df.loc[device_status_df['Room'] == room_fans, 'Fans'].values[0]
        
        if mode:
            if st.button(f"Toggle Fan in {room_fans}", key="fans_button"):
                new_status = "Off" if fan_status == "On" else "On"
                apply_manual_changes("Fans", room_fans, new_status)
                fan_status = new_status
                st.write(f"Fan toggled in {room_fans}.")
        
        # Status bubble
        st.markdown(f"**Current Fan Status:** {'🟢' if fan_status == 'On' else '🔴'} {fan_status}")

    col3, col4 = st.columns(2)
    with col3:
        st.image("window_icon.png", width=50)  # Original icon size
        st.write("#### Window Control")
        room_windows = st.selectbox("Select Room for Windows", ["Room 1", "Room 2", "Room 3", "Room 4"], key="windows")
        window_status = device_status_df.loc[device_status_df['Room'] == room_windows, 'Windows'].values[0]
        
        if mode:
            if st.button(f"Toggle Window in {room_windows}", key="windows_button"):
                new_status = "Closed" if window_status == "Open" else "Open"
                apply_manual_changes("Windows", room_windows, new_status)
                window_status = new_status
                st.write(f"Window status changed in {room_windows}.")
        
        # Status bubble
        st.markdown(f"**Current Window Status:** {'🟢' if window_status == 'Closed' else '🔴'} {window_status}")

    with col4:
        st.image("robot_icon.png", width=50)  # Original icon size
        st.write("#### Cleaning Robots")
        cleaning_robot_status = device_status_df.loc[device_status_df['Room'] == room_windows, 'CleaningRobot'].values[0]
        
        if mode:
            if st.button("Deploy Cleaning Robot", key="robot_button"):
                cleaning_robot_status = "Active"
                apply_manual_changes("CleaningRobot", room_windows, "Active")
                st.write("Cleaning robot deployed in all rooms.")
        
        # Status bubble
        st.markdown(f"**Cleaning Robot Status:** {'🟢' if cleaning_robot_status == 'Active' else '🔴'} {cleaning_robot_status}")

elif page == "Surveillance System":
    st.subheader("Surveillance System")
    st.write("View your home’s live surveillance feed and gas sensor status.")
    
    # Live feed placeholder (you can embed a camera feed here
        

    # Gas Sensor Data
    gas_levels = st.slider("Gas Sensor Levels", 0, 100)
    if gas_levels > 70:
        st.error("Dangerous gas levels detected!")
    # Load pre-trained data on face frontals from OpenCV (Haar cascade algorithm)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Function to trigger an alert
        # Add your code to send an email, trigger an alarm, etc.
    def trigger_alert_and_save(frame):
    # Print the alert message
        print("Intrusion Alert! Face Detected!")
    
    # Get the current time to name the photo uniquely
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create a directory to save the photos if it doesn't exist
        if not os.path.exists('intrusion_photos'):
            os.makedirs('intrusion_photos')
    
    # Save the frame as a photo
        file_name = f"intrusion_photos/intrusion_{timestamp}.jpg"
        cv2.imwrite(file_name, frame)
        print(f"Saved photo: {file_name}")
    # Start video capture from the default camera (0)
    last_detected_faces = []
    last_photo_time = 0
    photo_interval = 5 
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    stop_button_pressed = st.button("Stop")
    while True:
        
        # Read the current frame from the video capture
        ret, frame = cap.read()

        # Convert the frame to grayscale (Haar cascade requires grayscale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Process detected faces
        current_faces = []

        for idx, (x, y, w, h) in enumerate(faces):
            current_faces.append((x, y, w, h))

            # Draw a rectangle around the first face (normal detection)
            if idx == 0:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue box
                cv2.putText(frame, f"Face detected at {datetime.datetime.now()}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # If a second face is detected, mark as intruder and use a red box
            if idx == 1:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red box for intruder
                cv2.putText(frame, "Intruder!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Check the time interval to control photo capture frequency
            current_time = time.time()
            if (x, y, w, h) not in last_detected_faces and (current_time - last_photo_time > photo_interval):
                # Trigger intrusion alert and save the photo
                trigger_alert_and_save(frame)
                last_photo_time = current_time  # Update the last photo time

        # Update the list of last detected faces
            last_detected_faces = current_faces
            frame_placeholder.image(frame,channels="RGB")
            if cv2.waitKey(1) or 0xFF == ord("q") or stop_button_pressed:
                break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

    # Intruder Alert
    st.write("#### Intruder Alert System")
    intruder_status = st.radio("Intruder Status", ["Safe", "Alert"])
    if trigger_flag==1:
        st.warning("Intruder detected! Taking actions...")
    
elif page == "Pet Care System":
    st.subheader("Automatic Pet Care System")
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model(r"C:\\Users\\Lenovo\\AppData\\Local\\Microsoft\\WindowsApps\\SineWave\\Web\\keras_model.h5", compile=False)

    # Load the labels
    class_names = open(r"C:\\Users\\Lenovo\\AppData\\Local\\Microsoft\\WindowsApps\\SineWave\\Web\\labels.txt", "r").readlines()

    # CAMERA can be 0 or 1 based on default camera of your computer
    camera = cv2.VideoCapture(0)

    # Increase resolution (adjust as needed)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    frame_placeholder = st.empty()
    stop_button_pressed = st.button("Stop")
    while True:
        # Grab the webcamera's image.
        ret, image = camera.read()

        # Resize the raw image into (224-height,224-width) pixels for the model
        resized_image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Make the image a numpy array and reshape it to the models input shape.
        input_image = np.asarray(resized_image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        input_image = (input_image / 127.5) - 1

        # Predicts the model
        prediction = model.predict(input_image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Determine box color and label based on prediction
        if class_name.strip() == "0 dog":
            box_color = (0, 0, 255)  # Red for dog
            label = "DOG"
        elif class_name.strip() == "1 rabbit":
            box_color = (255, 255, 255)  # White for rabbit
            label = "RABBIT"
        else:
            box_color = (0, 255, 0)  # Green for other
            label = class_name.strip()

        # Draw rectangle and put text
        cv2.rectangle(image, (0, 0), (image.shape[1], image.shape[0]), box_color, 2)
        cv2.putText(image, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, box_color, 2)

        # Show the image in a window
        cv2.imshow("Pet Detector", image)
        frame_placeholder.image(image,channels="RGB")
        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        
        # Listen to the keyboard for presses.
        if cv2.waitKey(1) & 0xFF == ord('q')or stop_button_pressed:
            break

    camera.release()
    cv2.destroyAllWindows()
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
        # Simulate sensor data (replace with actual sensor API if available)
        def get_temperature():
            return random.uniform(18.0, 35.0)  # Simulate temperature (Celsius)

        def get_humidity():
            return random.uniform(30.0, 80.0)  # Simulate humidity (percentage)

        def get_gas_level():
            return random.choice(["normal", "elevated", "high"])  # Simulate gas level

        # Get all sensor data as a dictionary
        def get_sensor_data():
            return {
                "temperature": get_temperature(),
                "humidity": get_humidity(),
                "gas_level": get_gas_level()
            }

        # Chatbot processing
        def chatbot_response(user_input):
            sensor_data = get_sensor_data()
            if any(x in user_input.lower() for x in ["turn on", "turn off"]):
                return control_device(user_input)
            else:
                # Generate response using sensor data (as you had earlier)
                return f"Current conditions - Temperature: {sensor_data['temperature']:.2f}°C, Humidity: {sensor_data['humidity']:.2f}%, Gas Level: {sensor_data['gas_level']}."
        
        response = chatbot_response(user_input)
        st.write(f"House Insight Bot: {response}")
# Function to check device status based on room and device
def check_device_status(room, device):
    # Fetch the current status from the DataFrame
    status = device_status_df.loc[device_status_df['Room'] == room, device].values[0]
    return status

# Function to parse user commands and check for device status or control requests
def parse_device_command(user_input):
    user_input = user_input.lower()
    rooms = ["room 1", "room 2", "room 3", "room 4"]
    devices = ["lights", "fans", "windows", "cleaning robot"]

    # Check if user is asking for device status
    for room in rooms:
        for device in devices:
            if f"status of {device}" in user_input and room in user_input:
                status = check_device_status(room.title(), device.title())
                return f"The current status of {device} in {room} is: {status}."

    # Check if user is asking to turn a device on or off
    for room in rooms:
        for device in devices:
            if f"turn on {device}" in user_input and room in user_input:
                apply_manual_changes(device.title(), room.title(), "On")
                return f"{device.title()} in {room.title()} has been turned ON."
            elif f"turn off {device}" in user_input and room in user_input:
                apply_manual_changes(device.title(), room.title(), "Off")
                return f"{device.title()} in {room.title()} has been turned OFF."

    return None  # No matching command found

# Modified chatbot response function to handle device commands
#def chatbot_response(user_input, sensor_data):
    # First, check if the user input is related to device control or status
    #device_command_response = parse_device_command(user_input)
    #if device_command_response:
        #return device_command_response

    # If not a device command, continue with house status response
    #prompt = f"User: {user_input}\nThis house currently has the following conditions:\nTemperature: {sensor_data['temperature']:.2f}°C, Humidity: {sensor_data['humidity']:.2f}%, Gas Level: {sensor_data['gas_level']}."
def chatbot_response(user_input, sensor_data):
    # First, check if the user input is related to device control or status
    device_command_response = parse_device_command(user_input)
    if device_command_response:
        return device_command_response  # Return the device command response immediately

    # If not a device command, generate sensor status response
    return f"Current conditions - Temperature: {sensor_data['temperature']:.2f}°C, Humidity: {sensor_data['humidity']:.2f}%, Gas Level: {sensor_data['gas_level']}."
    generated_text = generator(
        prompt,
        max_length=50,  # Limit the length of the generated text
        num_return_sequences=1,
        temperature=0.7,  # Control randomness
        top_p=0.9,  # Use nucleus (top-p) sampling
        top_k=50  # Consider only the top 50 words for each generation step
    )[0]['generated_text']

    # Extract bot's reply
    bot_reply = generated_text.split("House Bot:")[-1].strip()

    # Add custom insights based on sensor data
    if sensor_data["temperature"] > 30:
        bot_reply += " The house feels quite warm. You might want to turn on the AC or fans to cool it down."
    elif sensor_data["temperature"] < 20:
        bot_reply += " The house feels cold. Consider increasing the heating or using a heater."

    if sensor_data["humidity"] > 60:
        bot_reply += " The humidity level in the house is high, which might feel uncomfortable. A dehumidifier could help."
    elif sensor_data["humidity"] < 40:
        bot_reply += " The air in the house is dry. Using a humidifier would improve comfort."

    if sensor_data["gas_level"]=="normal":
        bot_reply += " Caution: The gas levels are slightly elevated in the house. Ensure windows are open for proper ventilation."
    elif sensor_data["gas_level"] == "high":
        bot_reply += " WARNING: High gas levels detected! Take immediate action, ventilate the house, and ensure gas appliances are checked."

    return bot_reply



                

import streamlit as st
import pandas as pd

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

# Fetch current device status (automatic from backend)
device_status_df = fetch_device_status()

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

if page == "Home":
    st.write("Welcome to Sentinel! Your intelligent all-in-one home monitoring and control system.")
    
    # Display four tiles for Lights, Fans, Windows, and Cleaning Robots control in 4 rooms
    st.write(f"### Smart Device Control for 4 Rooms - Mode: {mode_name}")

    col1, col2 = st.columns(2)
    with col1:
        st.image("light_icon.png", width=100)  # Increased icon size
        st.write("#### Lights Control")
        room_lights = st.selectbox("Select Room for Lights", ["Room 1", "Room 2", "Room 3", "Room 4"], key="lights")
        light_status = device_status_df.loc[device_status_df['Room'] == room_lights, 'Lights'].values[0]
        
        if mode:
            if st.button(f"Toggle Lights in {room_lights}", key="lights_button"):
                new_status = "Off" if light_status == "On" else "On"
                device_status_df.loc[device_status_df['Room'] == room_lights, 'Lights'] = new_status
                light_status = new_status
                st.write(f"Lights toggled in {room_lights}.")
        
        # Status bubble
        st.markdown(f"**Current Light Status:** {'🟢' if light_status == 'On' else '🔴'} {light_status}")

    with col2:
        st.image("fan_icon.png", width=100)  # Increased icon size
        st.write("#### Fan Control")
        room_fans = st.selectbox("Select Room for Fan", ["Room 1", "Room 2", "Room 3", "Room 4"], key="fans")
        fan_status = device_status_df.loc[device_status_df['Room'] == room_fans, 'Fans'].values[0]
        
        if mode:
            if st.button(f"Toggle Fan in {room_fans}", key="fans_button"):
                new_status = "Off" if fan_status == "On" else "On"
                device_status_df.loc[device_status_df['Room'] == room_fans, 'Fans'] = new_status
                fan_status = new_status
                st.write(f"Fan toggled in {room_fans}.")
        
        # Status bubble
        st.markdown(f"**Current Fan Status:** {'🟢' if fan_status == 'On' else '🔴'} {fan_status}")

    col3, col4 = st.columns(2)
    with col3:
        st.image("window_icon.png", width=100)  # Increased icon size
        st.write("#### Window Control")
        room_windows = st.selectbox("Select Room for Windows", ["Room 1", "Room 2", "Room 3", "Room 4"], key="windows")
        window_status = device_status_df.loc[device_status_df['Room'] == room_windows, 'Windows'].values[0]
        
        if mode:
            if st.button(f"Toggle Window in {room_windows}", key="windows_button"):
                new_status = "Closed" if window_status == "Open" else "Open"
                device_status_df.loc[device_status_df['Room'] == room_windows, 'Windows'] = new_status
                window_status = new_status
                st.write(f"Window status changed in {room_windows}.")
        
        # Status bubble
        st.markdown(f"**Current Window Status:** {'🟢' if window_status == 'Closed' else '🔴'} {window_status}")

    with col4:
        st.image("robot_icon.png", width=100)  # Increased icon size
        st.write("#### Cleaning Robots")
        cleaning_robot_status = device_status_df.loc[device_status_df['Room'] == room_windows, 'CleaningRobot'].values[0]
        
        if mode:
            if st.button("Deploy Cleaning Robot", key="robot_button"):
                cleaning_robot_status = "Active"
                st.write("Cleaning robot deployed in all rooms.")
        
        # Status bubble
        st.markdown(f"**Cleaning Robot Status:** {'🟢' if cleaning_robot_status == 'Active' else '🔴'} {cleaning_robot_status}")

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
    
elif page == "Pet Care System":
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

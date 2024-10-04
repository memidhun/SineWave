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

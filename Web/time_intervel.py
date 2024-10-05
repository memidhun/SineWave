import cv2
import datetime
import os
import time

# Load pre-trained data on face frontals from OpenCV (Haar cascade algorithm)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to trigger an alert and save the photo
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
cap = cv2.VideoCapture(0)

# Variables to track timing and last detected faces
last_detected_faces = []
last_photo_time = 0
photo_interval = 5  # Time interval in seconds between photos

while True:
    # Read the current frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to grayscale (Haar cascade requires grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Process detected faces
    current_faces = []

    for (x, y, w, h) in faces:
        current_faces.append((x, y, w, h))
        
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Display the time of detection
        cv2.putText(frame, f"Face detected at {datetime.datetime.now()}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Check the time interval to control photo capture frequency
        current_time = time.time()
        if (x, y, w, h) not in last_detected_faces and (current_time - last_photo_time > photo_interval):
            # Trigger intrusion alert and save the photo
            trigger_alert_and_save(frame)
            last_photo_time = current_time  # Update the last photo time

    # Update the list of last detected faces
    last_detected_faces = current_faces

    # Display the frame with detection
    cv2.imshow('Intrusion Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

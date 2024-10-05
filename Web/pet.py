from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model(r"C:\Users\Midhun Mathew\Desktop\Test\Machine Learning\Model\Pet\keras_model.h5", compile=False)

# Load the labels
class_names = open(r"C:\Users\Midhun Mathew\Desktop\Test\Machine Learning\Model\Pet\labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    resized_image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the model's input shape.
    input_image = np.asarray(resized_image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    input_image = (input_image / 127.5) - 1

    # Predict using the model
    prediction = model.predict(input_image)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print(f"Class: {class_name}, Confidence Score: {str(np.round(confidence_score * 100))[:-2]}%")

    # Draw the frame and label based on prediction
    if index == 0:  # DOG
        cv2.rectangle(image, (0, 0), (image.shape[1], image.shape[0]), (0, 0, 255), 10)  # Red frame
        cv2.putText(image, "DOG", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)  # Red text
    elif index == 1:  # RABBIT
        cv2.rectangle(image, (0, 0), (image.shape[1], image.shape[0]), (0, 255, 0), 10)  # Green frame
        cv2.putText(image, "RABBIT", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)  # Green text
    elif index == 2:  # NEUTRAL
        pass  # No frame, no text

    # Display the frame with the label
    cv2.imshow("Webcam Image", image)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the ESC key.
    if keyboard_input == 27:
        break

# Release the camera and close the window
camera.release()
cv2.destroyAllWindows()

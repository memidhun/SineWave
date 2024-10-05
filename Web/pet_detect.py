from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
def pet_detect():
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model(r"C:\\Users\\Lenovo\\AppData\\Local\\Microsoft\\WindowsApps\\SineWave\\Web\\pet_model.h5", compile=False)

    # Load the labels
    class_names = open(r"C:\\Users\\Lenovo\\AppData\\Local\\Microsoft\\WindowsApps\\SineWave\\Web\\labels.txt", "r").readlines()

    # CAMERA can be 0 or 1 based on default camera of your computer
    camera = cv2.VideoCapture(0)

    # Increase resolution (adjust as needed)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break

    camera.release()
    cv2.destroyAllWindows()
pet_detect()

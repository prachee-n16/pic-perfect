import mediapipe as mp
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


async def hand_detection(rover):
    # Use MediaPipe to draw the hand frameword over the hands it identifies in synchronous
    hands_module = mp.solutions.hands
    draw_module = mp.solutions.drawing_utils

    # Use OpenCV to create a Video stream and add some values
    camera = rover.camera

    # intiate model
    model = load_model("mp_hand_gesture")
    file = open("gesture.names", "r")
    classNames = file.read().split("\n")
    file.close()

    # We add confidence values and extra settings to MediaPipe hand tracking. Since this is a live video stream and not static
    # image mode, confidence values in regards to overall detection and tracking and we will only let one hands be tracked at a time
    with hands_module.Hands(
        static_image_mode=False,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
        max_num_hands=1,
    ) as hands:
        while True:
            frame = await camera.get_image()
            if frame is None:
                print("Error capturing image.")
                break

            # save it in local
            file_path = "../../images/test_image_hand_recognition.jpg"
            with open(file_path, "wb") as f:
                f.write(frame.data)

            # get a cv2 version of the frame
            frame = cv2.imread(file_path)

            # for balance between speed and accurate and identification
            refined_frame = cv2.resize(frame, (640, 480))
            x, y, c = refined_frame.shape

            # Produces the hand framework overlay ontop of the hand
            result = hands.process(cv2.cvtColor(refined_frame, cv2.COLOR_BGR2RGB))

            className = ""

            if result.multi_hand_landmarks:
                Landmarks = []
                for hand_landmarks in result.multi_hand_landmarks:
                    for lm in hand_landmarks.landmark:
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)

                        Landmarks.append([lmx, lmy])

                    # Drawing landmarks on frames
                    draw_module.draw_landmarks(
                        refined_frame,
                        hand_landmarks,
                        hands_module.HAND_CONNECTIONS,
                    )

                    # Predict gesture
                    prediction = model.predict([Landmarks])
                    classID = np.argmax(prediction)
                    className = classNames[classID]

            if className == "thumbs up":
                print("Time to start capturing pictures!")
                break

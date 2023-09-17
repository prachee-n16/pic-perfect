import asyncio
import cv2
import imutils
import json
import mediapipe as mp
import numpy as np
import random
import tensorflow as tf
import time

from tensorflow.keras.models import load_model
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.vision import VisionClient

from Rover import Rover
from hand_recognition import hand_detection

VELOCITY = 250


async def connect():
    with open("../key.json", "r") as f:
        payload = json.load(f)["payload"]
    creds = Credentials(type="robot-location-secret", payload=payload)
    opts = RobotClient.Options(
        refresh_interval=0, dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address("htn-main.3o4e4wpz0f.viam.cloud", opts)


def leftOrRight(face_cascade, midpoint, frame_size, withinRange):
    min_face_size = 50  # Adjust this based on your requirements

    largest_area = 0
    largest = ()
    image = cv2.imread("img.jpeg")
    # Convert into grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) == 0:
        print("nothing detected")
        return [-1]

    # Draw rectangle around the faces
    for face in faces:
        (x, y, w, h) = face
        a = w*h
        if a > largest_area:
            largest_area = a
            largest = face
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    (x, y, w, h) = largest
    # Need to test this stop logic here, will this even work?
    if w >= min_face_size and h >= min_face_size:
        x_within_range = x <= 0.10 * \
            frame_size[0] and x + w >= 0.90 * frame_size[0]
        y_within_range = y <= 0.10 * \
            frame_size[1] and y + h >= 0.90 * frame_size[1]
        # print(x_within_range, y_within_range)
        # print(0.01 *
        #       frame_size[0])
        # print(x + w >= 0.99 * frame_size[0])
        # print(y <= 0.01 *
        #       frame_size[1])
        # print(y + h >= 0.99 * frame_size[1])
        if x_within_range and y_within_range:
            withinRange[0] = 1

    cx = (x + (x + w))/2
    if (cx < (midpoint - (midpoint/6))):
        return [0]
    if (cx > (midpoint + (midpoint/6))):
        return [2]
    elif y + h >= 0.90 * frame_size[1]:
        return [3]
    else:
        return [1]


async def main():
    robot = await connect()
    
    # Create instance of the rover class
    my_rover = Rover(robot)

    print("Robot Connected!")
    print("Resources:")
    print(robot.resource_names)

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Use MediaPipe to draw the hand frameword over the hands it identifies in synchronous
    hands_module = mp.solutions.hands
    draw_module = mp.solutions.drawing_utils

    # Use OpenCV to create a Video stream and add some values
    camera = my_rover.camera

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
            pastMove = ""

            frame = await camera.get_image()
            if frame is not None:
                file_path = "img.jpeg"
                with open(file_path, "wb") as f:
                    f.write(frame.data)
            else:
                print("Error capturing image.")
                break

            frame1 = await my_rover.camera.get_image(mime_type="image/jpeg")
            if frame1 is None:
                print("Error capturing image.")
                break

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

            withinRange = [0]
            takePicture = False

            if className == "thumbs up":
                print("Time to start capturing pictures!")
                takePicture = True
                withinRange[0] = 1

            if withinRange[0] != 1:
                answer = leftOrRight(
                    face_cascade, frame1.size[0]/2, frame1.size, withinRange
                )
            if withinRange[0] != 1:
                if answer[0] == 0:
                    # print("left")
                    # CCW is positive
                    pastMove = "left"
                    await my_rover.base.spin(angle=5, velocity=VELOCITY)
                    await my_rover.base.move_straight(distance=5, velocity=VELOCITY)
                elif answer[0] == 1:
                    # print("center")
                    pastMove = "center"
                    await my_rover.base.move_straight(distance=10, velocity=VELOCITY)
                elif answer[0] == 2:
                    # print("right")
                    pastMove = "right"
                    await my_rover.base.spin(angle=-5, velocity=VELOCITY)
                    await my_rover.base.move_straight(distance=5, velocity=VELOCITY)
                elif answer[0] == 3:
                    pastMove = "center"
                    await my_rover.base.move_straight(distance=-10, velocity=VELOCITY)
                elif answer[0] == -1:
                    if (pastMove == ""):
                        print("Randomly moving to look for objects.")
                        # Generate random movements (example: forward, backward, left, right)
                        random_movement = random.choice(
                            ["forward", "backward", "left", "right"])
                        if random_movement == "forward":
                            await my_rover.base.move_straight(distance=10, velocity=VELOCITY)
                        elif random_movement == "backward":
                            await my_rover.base.move_straight(distance=-10, velocity=VELOCITY)
                        elif random_movement == "left":
                            await my_rover.base.spin(angle=5, velocity=VELOCITY)
                        elif random_movement == "right":
                            await my_rover.base.spin(angle=-5, velocity=VELOCITY)
                    elif (pastMove == "right"):
                        await my_rover.base.spin(angle=5, velocity=VELOCITY)
                        pastMove = ""
                    elif (pastMove == "left"):
                        await my_rover.base.spin(angle=-5, velocity=VELOCITY)
                        pastMove = ""
                    elif (pastMove == "center"):
                        await my_rover.base.move_straight(distance=-10, velocity=VELOCITY)
                        pastMove = ""
                    else:
                        await my_rover.base.move_straight(distance=10, velocity=VELOCITY)
                        pastMove = ""
            else:
                print('STOP!')
                await my_rover.base.stop()

            if takePicture:
                for _ in range(5):
                    time.sleep(1)
                    await my_rover.base.stop()
                img = await my_rover.camera.get_image()
                if img is not None:
                    with open("capture.jpeg", "wb") as f:
                        f.write(img.data)
                else:
                    print("Error capturing image.")
                    break

    # close the robot when you're done!
    del my_rover


if __name__ == "__main__":
    asyncio.run(main())

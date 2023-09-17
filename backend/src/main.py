import asyncio
import cv2
import imutils

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera
from viam.components.base import Base
import json
import random  # Import the random module


async def connect():
    with open("./key.json", "r") as f:
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
    image = cv2.imread('img.jpeg')
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

    cv2.imwrite('border_img.jpeg', image)

    (x, y, w, h) = largest
    # Need to test this stop logic here, will this even work?
    if w >= min_face_size and h >= min_face_size:
        x_within_range = x <= 0.01 * \
            frame_size[0] and x + w >= 0.99 * frame_size[0]
        y_within_range = y <= 0.01 * \
            frame_size[1] and y + h >= 0.99 * frame_size[1]
        print(x_within_range, y_within_range)
        print(0.01 *
              frame_size[0])
        print(x + w >= 0.99 * frame_size[0])
        print(y <= 0.01 *
              frame_size[1])
        print(y + h >= 0.99 * frame_size[1])
        if x_within_range and y_within_range:
            withinRange = 1

    cx = (x + (x + w))/2
    if (cx < (midpoint - (midpoint/6))):
        return [0]
    if (cx > (midpoint + (midpoint/6))):
        return [2]
    else:
        return [1]


async def main():
    numCycles = 200      # run the loop X times
    vel = 250            # go this fast when moving motor
    robot = await connect()

    roverBase = Base.from_robot(robot, "viam_base")
    camera = Camera.from_robot(robot=robot, name="cam2")

    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    print("Robot Connected!")
    print("Resources:")
    print(robot.resource_names)
    # Main loop. Detect the ball, determine if it's on the left or right, and head that way.
    # Repeat this for until we have a good picture

    # Add the logic where this rover should keep moving until
    # it sees that person is not in frame
    for i in range(numCycles):
        pastMove = ""
        # Let's write a code which checks if the area of the face that was recognized makes up for a good chunk compared to frame ratio
        # Then, we will see whether or not this is near center of screen
        # If these two things are fulfilled, we can keep going.
        frame = await camera.get_image()
        frame1 = await camera.get_image(mime_type="image/jpeg")
        if frame is not None:
            # Convert frame to a format that can be saved
            file_path = "img.jpeg"
            with open(file_path, "wb") as f:
                f.write(frame.data)
        withinRange = 0
        answer = leftOrRight(
            face_cascade, frame1.size[0]/2, frame1.size, withinRange)
        if withinRange != 1:
            if answer[0] == 0:
                # print("left")
                # CCW is positive
                pastMove = "left"
                await roverBase.spin(angle=5, velocity=vel)
                await roverBase.move_straight(distance=100, velocity=vel)
            elif answer[0] == 1:
                # print("center")
                pastMove = "center"
                await roverBase.move_straight(distance=200, velocity=vel)
            elif answer[0] == 2:
                # print("right")
                pastMove = "right"
                await roverBase.spin(angle=-5, velocity=vel)
                await roverBase.move_straight(distance=100, velocity=vel)
            elif answer[0] == -1:
                if (pastMove == ""):
                    print("Randomly moving to look for objects.")
                    # Generate random movements (example: forward, backward, left, right)
                    random_movement = random.choice(
                        ["forward", "backward", "left", "right"])
                    if random_movement == "forward":
                        await roverBase.move_straight(distance=200, velocity=vel)
                    elif random_movement == "backward":
                        await roverBase.move_straight(distance=-200, velocity=vel)
                    elif random_movement == "left":
                        await roverBase.spin(angle=5, velocity=vel)
                    elif random_movement == "right":
                        await roverBase.spin(angle=-5, velocity=vel)
                elif (pastMove == "right"):
                    await roverBase.spin(angle=5, velocity=vel)
                    pastMove = ""
                elif (pastMove == "left"):
                    await roverBase.spin(angle=-5, velocity=vel)
                    pastMove = ""
                elif (pastMove == "center"):
                    pastMove = ""
        else:
            print('STOP!')
            await base.stop()
        # If nothing is detected, nothing moves

    # print("picture is ", frame)

    # get the parameters for a better picture clicked, so the web
    # cam can click a better one

    # Don't forget to close the robot when you're done!s
    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())

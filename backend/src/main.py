import asyncio
import cv2
import imutils

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera
from viam.components.base import Base
import json


async def connect():
    with open("./key.json", "r") as f:
        payload = json.load(f)["payload"]
    creds = Credentials(type="robot-location-secret", payload=payload)
    opts = RobotClient.Options(
        refresh_interval=0, dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address("htn-main.3o4e4wpz0f.viam.cloud", opts)


def leftOrRight(face_cascade, midpoint):
    largest_area = 0
    largest = ()
    image = cv2.imread('img.jpeg')
    # Convert into grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) == 0:
        print("nothing detected")
        return -1

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
    cx = (x + (x + w))/2
    if (cx < (midpoint - (midpoint/6))):
        return 0
    if (cx > (midpoint + (midpoint/6))):
        return 2
    else:
        return 1


async def main():
    numCycles = 200      # run the loop X times
    vel = 500            # go this fast when moving motor
    robot = await connect()

    roverBase = Base.from_robot(robot, "viam_base")
    camera = Camera.from_robot(robot=robot, name="cam")

    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    print("Robot Connected!")
    print("Resources:")
    print(robot.resource_names)
    # Main loop. Detect the ball, determine if it's on the left or right, and head that way.
    # Repeat this for until we have a good picture

    for i in range(numCycles):
        frame = await camera.get_image()
        frame1 = await camera.get_image(mime_type="image/jpeg")
        if frame is not None:
            # Convert frame to a format that can be saved
            file_path = "img.jpeg"
            with open(file_path, "wb") as f:
                f.write(frame.data)

        answer = leftOrRight(face_cascade, frame1.size[0]/2)

        if answer == 0:
            print("left")
            await roverBase.spin(angle=5, velocity=vel)     # CCW is positive
            await roverBase.move_straight(distance=600, velocity=vel)
        if answer == 1:
            print("center")
            await roverBase.move_straight(distance=600, velocity=vel)
        if answer == 2:
            print("right")
            await roverBase.spin(angle=-5, velocity=vel)
        # If nothing is detected, nothing moves

    # print("picture is ", frame)

    # get the parameters for a better picture clicked, so the web
    # cam can click a better one

    # Don't forget to close the robot when you're done!s
    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())

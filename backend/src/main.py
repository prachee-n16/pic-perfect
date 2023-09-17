import asyncio
from Rover import Rover
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.vision import VisionClient
from hand_recognition import hand_detection
import json


async def connect():
    with open("../key.json", "r") as f:
        payload = json.load(f)["payload"]
    creds = Credentials(type="robot-location-secret", payload=payload)
    opts = RobotClient.Options(
        refresh_interval=0, dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address("htn-main.3o4e4wpz0f.viam.cloud", opts)


# Check if this works?


async def stop_robot(base):
    # This is to stop the robot from moving :P
    await base.stop()


# Not passing in frame just yet but taking it within module
# Change design as fit later on
# This will run in a while loop initially? just to make sure we can get the person in frame


async def is_person_in_center_frame(camera, detector):
    frame = await camera.get_image(mime_type="image/jpeg")
    x, y = frame.size[0], frame.size[1]

    # Crop the image to get only the middle fifth of the top third of the original image
    cropped_frame = frame.crop((x / 2.5, 0, x / 1.25, y / 3))

    detections = await detector.get_detections(cropped_frame)

    if detections != []:
        return True
    return False


async def main():
    robot = await connect()
    # Call to the rover class
    my_rover = Rover(robot)
    print("Robot Connected!")
    print("Resources:")
    print(robot.resource_names)
    await hand_detection(my_rover)

    # take pictures and send it to ML model for better accurcy
    # frame = await my_rover.capture_image(5)
    # peopleClassifier - need to upload this model onto that
    peopleDetector = VisionClient.from_robot(robot, "person-detection")

    # Get detections and stuff
    # subject = await peopleDetector.get_detections(frame)
    # print(subject)

    # close the robot when you're done!
    del my_rover


if __name__ == "__main__":
    asyncio.run(main())

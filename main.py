import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera
import json


async def connect():
    with open("key.json", "r") as f:
        payload = json.load(f)["payload"]
    creds = Credentials(type="robot-location-secret", payload=payload)
    opts = RobotClient.Options(
        refresh_interval=0, dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address("htn-main.3o4e4wpz0f.viam.cloud", opts)


async def main():
    robot = await connect()

    print("Robot Connected!")
    print("Resources:")
    print(robot.resource_names)

    # take a picture and send it to ML model for better accurcy
    my_camera = Camera.from_robot(robot=robot, name="cam")
    frame = await my_camera.get_image()

    print("picture is ", frame)

    # get the parameters for a better picture clicked, so the web
    # cam can click a better one

    # Don't forget to close the robot when you're done!
    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())

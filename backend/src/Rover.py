from viam.components.base import Base
from viam.components.camera import Camera
from viam.errors import ResourceNotFoundError

class Rover:
    def __init__(self, robot):
        self.robot = robot
        try:
            self.camera = Camera.from_robot(robot=robot, name="cam")
        except ResourceNotFoundError:
            self.camera = Camera.from_robot(robot=robot, name="cam2")
        self.base = Base.from_robot(robot, "viam_base")

    async def capture_image(self, image_count):
        # take a picture and send it to ML model for better accurcy
        for i in range(image_count):
            frame = await self.camera.get_image()
            if frame is not None:
                # Convert frame to a format that can be saved
                file_path = f"../../images/test_image_{i}.jpg"
                await self.base.spin(velocity=100, angle=63)
                with open(file_path, "wb") as f:
                    f.write(frame.data)
            else:
                print("Error cannot capture picture")
        return

    def __del__(self):
        self.robot.close()

import airsim
import os

class AirSimWrapper:
    def __init__(self):
        ip = os.getenv('PX4_SIM_HOST_ADDR', '192.168.64.1')
        port = int(os.getenv('PX4_SIM_PORT', '41451'))
        print(f"Connecting to AirSim server at {ip}:{port}")
        self.client = airsim.VehicleClient(ip=ip, port=port)
        try:
            self.client.confirmConnection()
            print("Connection to AirSim successful!")
        except Exception as e:
            print(f"Failed to connect to AirSim: {e}")
            raise
    def get_camera_pose(self):
        return self.client.simGetVehiclePose()

    def set_camera_pose(self, pose):
        self.client.simSetVehiclePose(pose, True)

    def list_scene_objects(self):
        return self.client.simListSceneObjects()

    def get_position(self, object_name):
        object_names_ue = self.client.simListSceneObjects(object_name + ".*")
        if not object_names_ue:
            print(f"Object '{object_name}' not found in the scene.")
            return None
        pose = self.client.simGetObjectPose(object_names_ue[0])
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]
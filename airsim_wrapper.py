import airsim
import os
import logging
import math

logger = logging.getLogger(__name__)

class AirSimWrapper:
    def __init__(self):
        ip = os.getenv('PX4_SIM_HOST_ADDR', '192.168.64.1')  # Change IP if necessary
        port = int(os.getenv('PX4_SIM_PORT', '41451'))
        logger.info(f"Connecting to AirSim server at {ip}:{port}")
        self.client = airsim.VehicleClient(ip=ip, port=port)
        try:
            self.client.confirmConnection()
            logger.info("Connection to AirSim successful!")
        except Exception as e:
            logger.error(f"Failed to connect to AirSim: {e}")
            raise
        
    def get_camera_pose(self):
        try:
            return self.client.simGetVehiclePose()
        except Exception as e:
            logger.error(f"Error getting camera pose: {e}")
            return None

    def set_camera_pose(self, pose):
        try:
            self.client.simSetVehiclePose(pose, True)
        except Exception as e:
            logger.error(f"Error setting camera pose: {e}")

    def list_scene_objects(self):
        try:
            return self.client.simListSceneObjects()
        except Exception as e:
            logger.error(f"Error listing scene objects: {e}")
            return []
    
    def get_position(self, object_name):
        try:
            object_names_ue = self.client.simListSceneObjects(object_name + ".*")
            if not object_names_ue:
                logger.warning(f"Object '{object_name}' not found in the scene.")
                return None
            pose = self.client.simGetObjectPose(object_names_ue[0])
            return [pose.position.x_val, pose.position.y_val, pose.position.z_val]
        except Exception as e:
            logger.error(f"Error getting position of {object_name}: {e}")
            return None
        
    def get_distance_to_object(self, object_name):
        object_position = self.get_position(object_name)
        if object_position is None:
            return float('inf')  # Return an infinite distance if the object is not found
        
        camera_pose = self.get_camera_pose()
        if camera_pose is None:
            return float('inf') # Return an infinite distance if the camera pose is not found
        
        camera_position = [camera_pose.position.x_val, camera_pose.position.y_val, camera_pose.position.z_val]
        distance = math.sqrt(
            (camera_position[0] - object_position[0]) ** 2 +
            (camera_position[1] - object_position[1]) ** 2 +
            (camera_position[2] - object_position[2]) ** 2
        )
        return distance
        
        
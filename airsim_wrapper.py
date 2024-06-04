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
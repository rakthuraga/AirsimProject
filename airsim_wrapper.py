import airsim
import os
import logging
import math

logger = logging.getLogger(__name__)

class AirSimWrapper:
    def __init__(self):
        ip = os.getenv('PX4_SIM_HOST_ADDR', '192.168.64.1')  # Change IP if necessary
        
        logger.info(f"Connecting to AirSim server at {ip}:{port}")
        self.client = airsim.VehicleClient(ip=ip, port=port)
        try:
            self.client.confirmConnection()
            logger.info("Connection to AirSim successful!")
        except Exception as e:
            logger.error(f"Failed to connect to AirSim: {e}")
            raise
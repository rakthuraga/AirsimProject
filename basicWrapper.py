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
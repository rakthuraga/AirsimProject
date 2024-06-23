#import setup_path
import airsim

import pprint
import os
import time
import math
import tempfile
import numpy as np

radius = 20
altitude = 1

client = airsim.VehicleClient()
client.confirmConnection()

tmp_dir = os.path.join(r'D:\\SyntheticData\\DroneDek')
print ("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0)), True)
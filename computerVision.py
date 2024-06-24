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

max_altitude=30
min_altitude=1
altitude_steps=10
steps = 60

randomize_los_angle=False

min_radius=5
max_radius=10
radii_steps=5

altitudes = np.linspace(min_altitude,max_altitude, altitude_steps)
radii = np.linspace(min_radius, max_radius, radii_steps)

for alt_idx, altitude in enumerate(altitudes):
    for rad_idx, radius in enumerate(radii):

        percent_complete=((alt_idx+1)*(rad_idx+1))/(radii_steps*altitude_steps)*100
        print(percent_complete)
        print('{:.2f}% complete'.format(percent_complete))
        thetas=np.linspace(np.pi,3*np.pi,steps)
        x_coords = radius*np.cos(thetas)
        y_coords = radius*np.sin(thetas)
        pitch=np.arctan2(-1*altitude,radius)
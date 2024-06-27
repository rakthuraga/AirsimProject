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

        camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))
        client.simSetCameraPose("2", camera_pose)
        #client.simSetCameraPose("3", camera_pose)

        print("Altitude={}, Radius={}".format(altitude, radius))

        for step in range(steps):
            x = x_coords[step]
            y = y_coords[step]

       
            yaw=thetas[step]+np.pi

            if randomize_los_angle:
                yaw+=np.deg2rad(np.random.randint(-150,150)/10)
                pitch+=np.deg2rad(np.random.randint(-150,150)/10)

            orientation=airsim.to_quaternion(pitch, 0, yaw)
            client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(x, y, -1*altitude), orientation), True)


            responses = client.simGetImages([airsim.ImageRequest("2", airsim.ImageType.Segmentation),airsim.ImageRequest("2", airsim.ImageType.Scene)])
           
            for i, response in enumerate(responses):
                filename = os.path.join(tmp_dir, '{}_{}_{}_{}'.format(i,alt_idx,rad_idx,step))
                if response.pixels_as_float:
                    airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
                else:
                    airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
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
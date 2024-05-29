from openai import OpenAI
import re
import argparse
from airsim_wrapper import AirSimWrapper
import os
import json
import time

# Set up argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--prompt", type=str, default="prompts/airsim_basic.txt")
parser.add_argument("--sysprompt", type=str, default="system_prompts/airsim_basic.txt")
args = parser.parse_args()

# Load OpenAI API Key from config
with open("config.json", "r") as f:
    config = json.load(f)

print("Initializing ChatGPT...")
client = OpenAI(api_key=config["OPENAI_API_KEY"])

# Read system prompt
with open(args.sysprompt, "r") as f:
    sysprompt = f.read()

chat_history = [
    {
        "role": "system",
        "content": sysprompt
    },
    {
        "role": "user",
        "content": "move camera 10 units up"
    },
    {
        "role": "assistant",
        "content": """```python
import airsim     
current_pose = aw.get_camera_pose()
new_pose = airsim.Pose(current_pose.position + airsim.Vector3r(0, 0, -10), current_pose.orientation)
aw.set_camera_pose(new_pose)
This code gets the current camera pose using get_camera_pose(), modifies the Z coordinate to move the camera 10 units up, and then sets the new camera pose using set_camera_pose()."""
    }
]
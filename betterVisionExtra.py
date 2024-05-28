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
import logging
from openai import OpenAI
import airsim
import re
import argparse
from wrapper import AirSimWrapper
import os
import json
import time
import subprocess

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--prompt", type=str, default="prompts/airsim_basic.txt")
parser.add_argument("--sysprompt", type=str, default="system_prompts/airsim_basic.txt")
args = parser.parse_args()

# Load OpenAI API Key from config
with open("config.json", "r") as f:
    config = json.load(f)

logger.info("Initializing ChatGPT...")
client = OpenAI(api_key=config["OPENAI_API_KEY"])
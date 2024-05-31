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

def ask(prompt):
    chat_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=chat_history,
    temperature=0)
    chat_history.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content,
        }
    )
    return chat_history[-1]["content"]

print(f"Done.")

code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)

def extract_python_code(content):
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        full_code = "\n".join(code_blocks)

        if full_code.startswith("python"):
            full_code = full_code[7:]

        return full_code
    else:
        return None
    
class colors: # You may need to change color settings
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"

print(f"Initializing AirSim...")
aw = AirSimWrapper()
print(f"Done.")
with open(args.prompt, "r") as f:
    prompt = f.read()

ask(prompt)
print("Welcome to the AirSim chatbot! I am ready to help you with your AirSim questions and commands.")

while True:
    question = input(colors.YELLOW + "AirSim> " + colors.ENDC)

    if question == "!quit" or question == "!exit":
        break

    if question == "!clear":
        os.system("cls")
        continue

    response = ask(question)

    print(f"\n{response}\n")

    code = extract_python_code(response)
    if code is not None:
        print("Please wait while I run the code in AirSim...")
        exec(extract_python_code(response))
        print("Done!\n")
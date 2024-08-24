# ai_scene_recognition

Add config.json file with following code:
{
    "OPENAI_API_KEY": "fill in with your openai key (must be able to support gpt-4o )"
}

BomboOrig.py:
This file takes in an image (screenshot from airsim unreal MidWestWorld environment) and analyzes the image using openai api.This file also includes functions to extract the keywords and coordinates from the response to the given prompt. Make sure to use your gpt 4 openai api key.

baseGpt.py:
This file is the main code which allows openai api to connect to MidWestWorld environment and convert your prompt directly into airsim code done by the openai api. This code is then ran in the airsim and midwestworld environment in Unreal
engine 4 and causes the drone to move around based on the given code. This is
accomplished by using the file wrapper.py which serves as an airsim wrapper
used by openai api. The drone is also able to use screenshots of the MidWestWorld
environment to avoid obstacles which is achieved by gptHelper.py.

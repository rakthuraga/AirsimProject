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
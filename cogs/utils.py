import json
import os

# File paths
DATA_FOLDER = "data"
TEAM_FILE = os.path.join(DATA_FOLDER, "teams.json")
XP_FILE = os.path.join(DATA_FOLDER, "xp.json")
SCRIM_FILE = os.path.join(DATA_FOLDER, "scrims.json")

# Ensure data folder and files exist
os.makedirs(DATA_FOLDER, exist_ok=True)

for file in [TEAM_FILE, XP_FILE, SCRIM_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)

# JSON helpers
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Specific file helpers
def load_teams():
    return load_json(TEAM_FILE)

def save_teams(data):
    save_json(TEAM_FILE, data)

def load_xp():
    return load_json(XP_FILE)

def save_xp(data):
    save_json(XP_FILE, data)

def load_scrims():
    return load_json(SCRIM_FILE)

def save_scrims(data):
    save_json(SCRIM_FILE, data)

# XP Level calculation helper
def calculate_level(xp):
    return int(xp ** 0.5)

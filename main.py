import json
from pathlib import Path
from classes.Player import Player

BASE_DIR = Path(__file__).parent
PLAYER_DATA_FILE = BASE_DIR / "data" / "playerData.json"

running = True

actions = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None
}

try:
    with open(PLAYER_DATA_FILE, "r") as file:
        player = Player.from_dict(json.load(file))

except (FileNotFoundError, json.JSONDecodeError):
    name = input("Enter your character's name: ")
    player = Player(name, "Qi Refining", 1, 0, 100, 100, 10, 5)

    with open(PLAYER_DATA_FILE, "w") as file:
        json.dump(player.to_dict(), file, indent=4)

player.view_status()

with open(PLAYER_DATA_FILE, "w") as file:
    json.dump(player.to_dict(), file, indent=4)

# check if json is empty and user import, if not empty import thje file
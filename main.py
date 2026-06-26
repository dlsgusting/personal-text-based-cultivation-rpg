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
with open(PLAYER_DATA_FILE, "r") as file:
    data = json.load(file)

player = Player.from_dict(data)
player.view_status()
player.cultivate()

with open(PLAYER_DATA_FILE, "w") as file:
    json.dump(player.to_dict(), file, indent=4)
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
PLAYER_DATA_FILE = BASE_DIR / "data" / "playerData.json"

running = True

actions = {
    1: none,
    2: none,
    3: none,
    4: none,
    5: none
}

while running:

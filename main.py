import json
from pathlib import Path
from classes.Player import Player

BASE_DIR = Path(__file__).parent
PLAYER_DATA_FILE = BASE_DIR / "data" / "playerData.json"

running = True

try:
    with open(PLAYER_DATA_FILE, "r") as file:
        player = Player.from_dict(json.load(file))

except (FileNotFoundError, json.JSONDecodeError):
    name = input("Enter your character's name: ")
    player = Player(name, "Qi Refining", 1, 0, 100, 100, 10, 5)

    with open(PLAYER_DATA_FILE, "w") as file:
        json.dump(player.to_dict(), file, indent=4)

def exit_menu():
    global running
    running = False

actions = {
    1: player.view_status,
    2: player.cultivate,
    3: player.breakthrough,
    4: None,
    5: exit_menu
}

def choose_action():
    print("\n")
    print("1. View your stats")
    print("2. Cultivate")
    print("3. Realm breakthrough")
    print("4. TBA")
    print("5. Exit")

    valid = [1,2,3,5]

    while True:
        try:
            action = int(input())

            if action in valid:
                break
            else:
                print("Not a valid action, choose again")

        except ValueError:
            print("Please enter a valid action number.")

    return action



while running:
    selected = choose_action()
    actions[selected]()

    with open(PLAYER_DATA_FILE, "w") as file:
        json.dump(player.to_dict(), file, indent=4)


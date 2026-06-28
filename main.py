import json
import random
from pathlib import Path
from classes.Player import Player

BASE_DIR = Path(__file__).parent
PLAYER_DATA_FILE = BASE_DIR / "data" / "playerData.json"

BASE_DIR2 = Path(__file__).parent
EVENTS_FILE = BASE_DIR2 / "data" / "events.json"

BASE_DIR3 = Path(__file__).parent
ENEMIES_FILE = BASE_DIR2 / "data" / "enemies.json"

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

def choose_action():
    print("\n")
    print("1. View your stats")
    print("2. Cultivate")
    print("3. Realm breakthrough")
    print("4. Events")
    print("5. Exit")

    valid = [1,2,3,4,5]

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

def combat():
    realm_stages = {
    "Qi Refining": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "Foundation Establishment": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    "Golden Core": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    "Nascent Soul": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39]   
    }
    with open(ENEMIES_FILE, "r") as file:
        enemies = json.load(file)



    chosen_enemy = random.choice(realm_stages[player.realm])
    enemy1 = Enemy(chosen_enemy["name"], chosen_enemy["realm"], chosen_enemy["minor_realm"])


def event():
    with open(EVENTS_FILE, "r") as file:
        events = json.load(file)

    num = random.randint(1, 30)
    if num <= 4:
        combat()
        return
    chosen_event = random.choice(events)

    event_type = chosen_event["type"]
    print(chosen_event["description"])

    if event_type == "cultivate":
        qi_gain = chosen_event["reward"]["qi"]
        player.qi += qi_gain
        print(f"You gained {qi_gain} qi!")

    elif event_type == "loot":
        reward = chosen_event["reward"]

        if "spirit_stone" in reward:
            stones = reward["spirit_stone"]
            player.spirit_stone += stones
            print(f"You got {stones} spirit stones!")

        else:
            for key, value in reward.items():
                print(f"You got: {value} ({key})")



actions = {
    1: player.view_status,
    2: player.cultivate,
    3: player.breakthrough,
    4: event,
    5: exit_menu
}


while running:
    selected = choose_action()
    actions[selected]()

    with open(PLAYER_DATA_FILE, "w") as file:
        json.dump(player.to_dict(), file, indent=4)


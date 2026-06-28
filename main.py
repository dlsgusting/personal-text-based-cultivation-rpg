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
    player = Player(name, "Qi Refining", 1, 0, 100, 100, 100, 10, 2)

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

    valid_actions = [1, 2, 3]
    with open(ENEMIES_FILE, "r") as file:
        enemies = json.load(file)

    chosen_enemy = random.choice(realm_stages[player.realm])
    enemy1 = Enemy(chosen_enemy["name"], chosen_enemy["realm"]["major"], chosen_enemy["realm"]["minor"])
    enemy1.update_status()
    print(chosen_enemy["description"])
    combat = True
    p_counter = 0
    e_counter = 0

    while combat:
        p_counter -= 1
        e_counter -= 1
        if p_counter == 0:
            player1.defend_off()
        elif e_counter == 0:
            enemy1.defend_off()

        # player turn
        while True:
            try:
                action = int(input("Choose your action: 1. Attack 2. Defend 3. Heal: "))
                if action in valid_actions:
                    break
                else:
                    print("Not a valid action, choose again")
            except ValueError:
                print("Please enter a valid action number.")

        if action == 1:
            damage = player.attack - enemy1.defense
            if damage < 0:
                damage = 0
            enemy1.take_damage(damage)
            print(f"You dealt {damage} damage to {enemy1.name}!")
        elif action == 2:
            player.defend()
            p_counter = 2
            print(f"You raise your guard, increasing your defense to {player.defense}!")
        elif action == 3:
            player.heal()
            print(f"You healed yourself for {player.max_health * 0.15} health!")

        # enemy turn
        enemy_action = random.choice(valid_actions)
        if enemy_action == 1:
            damage = enemy1.attack - player.defense
            if damage < 0:
                damage = 0
            player.take_damage(damage)
            print(f"{enemy1.name} dealt {damage} damage to you!")
        elif enemy_action == 2:
            enemy1.defend()
            e_counter = 2
            print(f"{enemy1.name} raises its guard, increasing its defense to {enemy1.defense}!")
        elif enemy_action == 3:
            enemy1.heal()
            print(f"{enemy1.name} healed itself for {enemy1.max_health * 0.15} health!")

def event():
    with open(EVENTS_FILE, "r") as file:
        events = json.load(file)

    num = random.randint(1, 30)
    if num <= 30:
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


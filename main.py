import json
import random
from pathlib import Path
from classes.Player import Player
from classes.Enemy import Enemy

BASE_DIR = Path(__file__).parent

PLAYER_DATA_FILE = BASE_DIR / "data" / "playerData.json"
EVENTS_FILE = BASE_DIR / "data" / "events.json"
ENEMIES_FILE = BASE_DIR / "data" / "enemies.json"

running = True

try:
    with open(PLAYER_DATA_FILE, "r") as file:
        player1 = Player.from_dict(json.load(file))

except (FileNotFoundError, json.JSONDecodeError):
    name = input("Enter your character's name: ")
    player1 = Player(name, "Qi Refining", 1, 0, 0, 0, 0, 0, 0)
    player1.update_stats()
    player1.update_max_qi()

    with open(PLAYER_DATA_FILE, "w") as file:
        json.dump(player1.to_dict(), file, indent=4)

def exit_menu():
    global running
    running = False

def choose_action():
    print("\n")
    print("1. View your stats")
    print("2. Cultivate")
    print("3. Realm breakthrough")
    print("4. Events")
    print("5. Combat")
    print("6. Exit")

    valid = [1,2,3,4,5,6]

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

def finish_combat():
    player1.defend_off()
    player1.health = player1.max_health


def combat():
    valid_actions = [1, 2, 3]

    with open(ENEMIES_FILE, "r") as file:
        enemies = json.load(file)

    same_realm_enemies = [
        enemy for enemy in enemies
        if enemy["realm"]["major"] == player1.realm
    ]


    close_enemies = [
        enemy for enemy in same_realm_enemies
        if abs(enemy["realm"]["minor"] - player1.minor_realm) <= 3
    ]

    enemy_pool = close_enemies or same_realm_enemies or enemies
    chosen_enemy = random.choice(enemy_pool)

    enemy1 = Enemy(
        chosen_enemy["name"],
        chosen_enemy["realm"]["major"],
        chosen_enemy["realm"]["minor"]
    )

    enemy1.update_stats()
    print(chosen_enemy["description"])

    p_counter = 0
    e_counter = 0

    while True:
        if player1.health <= 0:
            print("You have been defeated!")
            finish_combat()

            qi_loss = int(player1.max_qi * 0.1)
            player1.qi = max(0, player1.qi - qi_loss)
            break

        if enemy1.health <= 0:
            print(f"You have defeated {enemy1.name}!")
            finish_combat()

            qi_gain = int(player1.max_qi * 0.1)
            player1.qi = min(player1.max_qi, player1.qi + qi_gain)
            break

 
        if p_counter > 0:
            p_counter -= 1
            if p_counter == 0:
                player1.defend_off()

        if e_counter > 0:
            e_counter -= 1
            if e_counter == 0:
                enemy1.defend_off()

        player1.view_status()
        enemy1.view_status()

        # Player turn
        while True:
            try:
                action = int(input("Choose your action: 1. Attack 2. Defend 3. Heal: "))

                if action == 3 and player1.health == player1.max_health:
                    print("You are already at full health!")
                elif action == 2 and p_counter > 0:
                    print("You are already defending!")
                elif action in valid_actions:
                    break
                else:
                    print("Not a valid action, choose again.")
            except ValueError:
                print("Please enter a valid action number.")

        if action == 1:
            damage = max(0, player1.attack - enemy1.defense)
            enemy1.take_damage(damage)
            print(f"You dealt {damage} damage to {enemy1.name}!")

        elif action == 2:
            player1.defend()
            p_counter = 2
            print(f"You raise your guard, increasing your defense to {player1.defense}!")

        elif action == 3:
            healed = player1.heal()
            print(f"You healed yourself for {healed} health!")

        if enemy1.health <= 0:
            continue

        # Enemy turn
        enemy_actions = [1]

        if e_counter == 0:
            enemy_actions.append(2)

        if enemy1.health < enemy1.max_health:
            enemy_actions.append(3)

        enemy_action = random.choice(enemy_actions)

        if enemy_action == 1:
            damage = max(0, enemy1.attack - player1.defense)
            player1.take_damage(damage)
            print(f"{enemy1.name} dealt {damage} damage to you!")

        elif enemy_action == 2:
            enemy1.defend()
            e_counter = 2
            print(f"{enemy1.name} raises its guard, increasing its defense to {enemy1.defense}!")

        elif enemy_action == 3:
            healed = enemy1.heal()
            print(f"{enemy1.name} healed itself for {healed} health!")

def event():
    with open(EVENTS_FILE, "r") as file:
        events = json.load(file)

    chosen_event = random.choice(events)

    event_type = chosen_event["type"]
    print(chosen_event["description"])

    if event_type == "cultivate":
        qi_gain = chosen_event["reward"]["qi"]
        player1.qi = min(player1.max_qi, player1.qi + qi_gain)
        print(f"You gained {qi_gain} qi!")

    elif event_type == "loot":
        reward = chosen_event["reward"]

        if "spirit_stone" in reward:
            stones = reward["spirit_stone"]
            player1.spirit_stone += stones
            print(f"You got {stones} spirit stones!")

        else:
            for key, value in reward.items():
                print(f"You got: {value} ({key})")



actions = {
    1: player1.view_status,
    2: player1.cultivate,
    3: player1.breakthrough,
    4: event,
    5: combat,
    6: exit_menu
}


while running:
    selected = choose_action()
    actions[selected]()

    with open(PLAYER_DATA_FILE, "w") as file:
        json.dump(player1.to_dict(), file, indent=4)


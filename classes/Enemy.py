import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REALM_DATA = BASE_DIR / "data" / "realmData.json"

with open(REALM_DATA, "r") as file:
    realms = json.load(file)

class Enemy:
    def __init__(
        self, 
        name, 
        realm,
        minor_realm
        ):
        self.name = name
        self.realm = realm
        self.minor_realm = minor_realm
        self.health = 1
        self.max_health = 1
        self.attack = 1
        self.defense = 1

    def view_status(self):
        print("\n")
        print(f"Name: {self.name}")
        print(f"Realm: {self.realm} {self.minor_realm}")    
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")

    def get_realm_data(self):
        current_realm_index = realms_dict[self.realm]
        return realms["realms"][current_realm_index]


    def update_stats(self):
        realm_data = self.get_realm_data()
        multiplier = realm_data["stage_multiplier"] ** (self.minor_realm - 1)

        self.health = int(realm_data["base_hp"] * multiplier)
        self.max_health = int(realm_data["base_hp"] * multiplier)
        self.attack = int(realm_data["base_attack"] * multiplier)
        self.defense = int(realm_data["base_defense"] * multiplier)

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def defend(self):
        self.defense += self.defense
    def defend_off(self):
        self.defense -= self.defense

    def heal(self):
        self.health = self.health + (self.max_health * 0.15)
        if self.health > self.max_health:
            self.health = self.max_health
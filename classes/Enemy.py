import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REALM_DATA = BASE_DIR / "data" / "realmData.json"

with open(REALM_DATA, "r") as file:
    realms = json.load(file)

realms_dict = {
    "Qi Refining" : 0,
    "Foundation Establishment" : 1,
    "Golden Core" : 2,
    "Nascent Soul" : 3
}

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
        self.is_defending = False

    def take_damage(self, damage):
        damage = max(0, int(damage))
        self.health -= damage

        if self.health < 0:
            self.health = 0


    def defend(self):
        if not self.is_defending:
            self.defense *= 2
            self.is_defending = True


    def defend_off(self):
        if self.is_defending:
            self.defense //= 2
            self.is_defending = False


    def heal(self):
        old_health = self.health
        heal_amount = int(self.max_health * 0.05)

        self.health = min(self.max_health, self.health + heal_amount)

        return self.health - old_health
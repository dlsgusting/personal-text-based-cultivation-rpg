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
class Player:
    def __init__(
        self, 
        name, 
        realm,
        minor_realm,
        qi,
        max_qi,
        health,
        max_health,
        attack,
        defense
        ):
        self.name = name
        self.realm = realm
        self.minor_realm = minor_realm
        self.qi = qi
        self.max_qi = max_qi
        self.health = health
        self.max_health
        self.attack = attack
        self.defense = defense

    def to_dict(self):
        return {
            "name": self.name,
            "realm": self.realm,
            "minor_realm": self.minor_realm,
            "qi": self.qi,
            "max_qi": self.max_qi,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "defense": self.defense
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["realm"],
            data["minor_realm"],
            data["qi"],
            data["max_qi"],
            data["health"],
            data["max_health"],
            data["attack"],
            data["defense"]
        )

    def view_status(self):

        print("\n")
        print(f"Name: {self.name}")
        print(f"Realm: {self.realm} {self.minor_realm}")    
        print(f"Qi: {self.qi}/{self.max_qi}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")

    def cultivate(self):
        if self.qi >= self.max_qi:
            self.qi = self.max_qi
            print("Already at max qi, can't go any higher.")
        else:
            self.qi += 100
        self.view_status()

    def get_realm_data(self):
        current_realm_index = realms_dict[self.realm]
        return realms["realms"][current_realm_index]


    def update_stats(self):
        realm_data = self.get_realm_data()
        multiplier = realm_data["stage_multiplier"] ** (self.minor_realm - 1)

        self.health = int(realm_data["base_hp"] * multiplier)
        self.max_health = self.health
        self.attack = int(realm_data["base_attack"] * multiplier)
        self.defense = int(realm_data["base_defense"] * multiplier)


    def update_max_qi(self):
        realm_data = self.get_realm_data()

        self.max_qi = (
            realm_data["breakthrough_qi_required"] + realm_data["breakthrough_qi_increase"] * (self.minor_realm - 1)
        )


    def minor_realm_inc(self):
        self.minor_realm += 1
        self.qi = 0

        self.update_stats()
        self.update_max_qi()


    def major_realm_increase(self):
        current_realm_index = realms_dict[self.realm]
        next_realm_index = current_realm_index + 1

        if next_realm_index >= len(realms["realms"]):
            print("You are already at the highest realm.")
            return

        self.realm = realms["realms"][next_realm_index]["name"]
        self.minor_realm = 1
        self.qi = 0

        self.update_stats()
        self.update_max_qi()
        

    def breakthrough(self):
        if self.qi < self.max_qi:
            print(f"Cannot breakthrough. Current qi: {self.qi}, required qi: {self.max_qi}")
            return

        if self.minor_realm < 10:
            self.minor_realm_inc()
            print(f"You broke through to {self.realm} {self.minor_realm}!")
        else:
            self.major_realm_increase()
            print(f"You broke through to {self.realm} {self.minor_realm}!")

        self.view_status()

    def take_damage(self, damage):
        if self.defense >= damage:
            print("Your defense is higher than enemy damage, attack nullified")
        else:
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



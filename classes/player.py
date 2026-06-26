import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REALM_DATA = BASE_DIR / "data" / "realmData.json"

with open(REALM_DATA, "r") as file:
    realms = json.load(file)

realms_dict = {
    "Qi Refining" : 0,
    "Foundation Establishment" : 1
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
        attack,
        defense
        ):
        self.name = name
        self.realm = realm
        self.minor_realm = minor_realm
        self.qi = qi
        self.max_qi = max_qi
        self.health = health
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
            data["attack"],
            data["defense"]
        )

    def minor_realm_inc(self):
        current_realm = realms_dict[self.realm]
        self.minor_realm += 1
        self.qi = 0
        self.max_qi += realms["realms"][current_realm]["breakthrough_qi_increase"]
        self.health += realms["realms"][current_realm]["hp_increase"]
        self.attack += realms["realms"][current_realm]["attack_increase"]
        self.defense += realms["realms"][current_realm]["defense_increase"]


    def view_status(self):
        print("\n")
        print(f"Name: {self.name}")
        print(f"Realm: {self.realm} {self.minor_realm}")    
        print(f"Qi: {self.qi}/{self.max_qi}")
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")

    def cultivate(self):
        self.qi += 100

    def breakthrough(self):
        if self.qi < self.max_qi :
            print(f"Cannot breakthrough. Current qi: {self.qi}, required qi: {self.max_qi}")
            return
        
        if self.realm == "Qi Refining" and self.minor_realm < 9:
            self.minor_realm_inc()

        
        




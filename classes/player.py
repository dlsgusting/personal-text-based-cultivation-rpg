import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REALM_DATA = BASE_DIR / "data" / "realmData.json"

with open(REALM_DATA, "r") as file:
    realms = json.load(file)

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

    def view_status(self):
        for attribute, value in self.__dict__.items():
         print(f"{attribute}: {value}")

    def cultivate(self):
        self.qi += 1




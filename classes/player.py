import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
REALM_DATA = BASE_DIR / "data" / "realmData.json"

with open("realms.json", "r") as file:
    data = json.load(file)

class player:
    def __init__(self,
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
        self.realm = mortal
        self.minor_realm = 0
        self.qi = 0
        self.max_qi = 10
        self.health = 100
        self.attack = 10
        self.defense = 5

    def cultivate(self):
        self.qi += 1

    def breakthrough(self):
        if self.qi == self.max_qi:


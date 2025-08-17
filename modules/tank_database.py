import os
import json
import random
from config import DATA_PATH

class TankDatabase:
    def __init__(self):
        self.data_file = os.path.join(DATA_PATH, "tanks.json")
        self.tanks = self.load_tanks()
    
    def load_tanks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        return []
    
    def get_tank(self, tank_id):
        for tank in self.tanks:
            if tank["id"] == tank_id:
                return tank
        return None
    
    def get_random_tank(self):
        return random.choice(self.tanks) if self.tanks else None
    
    def get_tanks_by_rarity(self, rarity):
        return [t for t in self.tanks if t["rarity"] == rarity]
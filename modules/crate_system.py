from .tank_database import TankDatabase
import random

class CrateSystem:
    def __init__(self):
        self.tank_db = TankDatabase()
        
    def open_crate(self):
        tank = self.tank_db.get_random_tank()
        return tank if tank else None
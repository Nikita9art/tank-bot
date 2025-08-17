from .tank_database import TankDatabase

class CollectionView:
    def __init__(self):
        self.tank_db = TankDatabase()
    
    def get_collection_details(self, collection):
        tanks = []
        for tank_id in collection:
            tank = self.tank_db.get_tank(tank_id)
            if tank:
                tanks.append(tank)
        return tanks
    
    def format_collection(self, collection):
        if not collection:
            return "Ваша коллекция пуста!"
            
        # Группировка по редкости
        groups = {}
        for tank in self.get_collection_details(collection):
            rarity = tank["rarity"]
            groups.setdefault(rarity, []).append(tank)
        
        # Формирование ответа
        response = "🏆 Ваша коллекция танков:\n\n"
        for rarity, tanks in groups.items():
            response += f"{rarity} ({len(tanks)}):\n"
            response += ", ".join(t["name"] for t in tanks[:3])
            if len(tanks) > 3:
                response += f" и ещё {len(tanks)-3}"
            response += "\n\n"
        
        return response
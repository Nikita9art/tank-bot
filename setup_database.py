import os
import json
import random

DATA_PATH = "/storage/emulated/0/Documents/танк бот/data/"

# Список реальных исторических танков с точными характеристиками
REAL_TANKS = [
    # Советские танки
    {"id": "T-34-76", "name": "T-34-76", "nation": "USSR", "type": "Medium", "year": 1940, 
     "armor": 45, "gun": "76.2 мм Л-11", "engine": "500 л.с.", "speed": 53, 
     "description": "Легендарный советский средний танк Великой Отечественной войны",
     "rarity": "Legendary", "price": 500000},
    
    {"id": "KV-1", "name": "КВ-1", "nation": "USSR", "type": "Heavy", "year": 1939, 
     "armor": 75, "gun": "76.2 мм ЗИС-5", "engine": "600 л.с.", "speed": 35, 
     "description": "Тяжелый танк прорыва с мощной бронезащитой", 
     "rarity": "Epic", "price": 450000},
    
    {"id": "IS-2", "name": "ИС-2", "nation": "USSR", "type": "Heavy", "year": 1943, 
     "armor": 120, "gun": "122 мм Д-25Т", "engine": "600 л.с.", "speed": 37, 
     "description": "Самый мощный серийный тяжелый танк Второй мировой", 
     "rarity": "Legendary", "price": 750000},
    
    # Немецкие танки
    {"id": "Tiger-I", "name": "Tiger I", "nation": "Germany", "type": "Heavy", "year": 1942, 
     "armor": 100, "gun": "88 мм KwK 36", "engine": "700 л.с.", "speed": 38, 
     "description": "Знаменитый немецкий тяжелый танк с мощной 88-мм пушкой", 
     "rarity": "Epic", "price": 700000},
    
    {"id": "Panther", "name": "Panther", "nation": "Germany", "type": "Medium", "year": 1943, 
     "armor": 80, "gun": "75 мм KwK 42", "engine": "700 л.с.", "speed": 46, 
     "description": "Один из лучших средних танков Второй мировой войны", 
     "rarity": "Epic", "price": 650000},
    
    # Американские танки
    {"id": "Sherman", "name": "M4 Sherman", "nation": "USA", "type": "Medium", "year": 1942, 
     "armor": 76, "gun": "75 мм M3", "engine": "400 л.с.", "speed": 40, 
     "description": "Самый массовый танк западных союзников во Второй мировой", 
     "rarity": "Common", "price": 300000},
    
    {"id": "Pershing", "name": "M26 Pershing", "nation": "USA", "type": "Heavy", "year": 1944, 
     "armor": 102, "gun": "90 мм M3", "engine": "500 л.с.", "speed": 40, 
     "description": "Американский тяжелый танк конца Второй мировой войны", 
     "rarity": "Rare", "price": 550000},
    
    # Британские танки
    {"id": "Cromwell", "name": "Cromwell", "nation": "UK", "type": "Medium", "year": 1943, 
     "armor": 76, "gun": "75 мм QF 75 mm", "engine": "600 л.с.", "speed": 64, 
     "description": "Быстрый и маневренный британский средний танк", 
     "rarity": "Uncommon", "price": 350000},
    
    {"id": "Churchill", "name": "Churchill", "nation": "UK", "type": "Heavy", "year": 1941, 
     "armor": 152, "gun": "75 мм QF 75 mm", "engine": "350 л.с.", "speed": 25, 
     "description": "Тяжело бронированный, но медленный пехотный танк", 
     "rarity": "Rare", "price": 400000},
    
    # Современные танки
    {"id": "T-90", "name": "T-90", "nation": "Russia", "type": "Main Battle", "year": 1992, 
     "armor": "Композитная", "gun": "125 мм 2A46M", "engine": "1130 л.с.", "speed": 65, 
     "description": "Современный российский основной боевой танк", 
     "rarity": "Epic", "price": 5000000},
    
    {"id": "Abrams", "name": "M1 Abrams", "nation": "USA", "type": "Main Battle", "year": 1980, 
     "armor": "Композитная", "gun": "120 мм M256", "engine": "1500 л.с.", "speed": 67, 
     "description": "Основной боевой танк США, один из лучших в мире", 
     "rarity": "Epic", "price": 6000000},
    
    {"id": "Leopard-2", "name": "Leopard 2", "nation": "Germany", "type": "Main Battle", "year": 1979, 
     "armor": "Композитная", "gun": "120 мм Rheinmetall", "engine": "1500 л.с.", "speed": 70, 
     "description": "Немецкий основной боевой танк, эталон надежности", 
     "rarity": "Epic", "price": 5500000},
]

def create_valid_json(file_path, default_content):
    """Создает файл с валидным JSON содержимым"""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                json.load(f)
            return
    except:
        pass
    
    with open(file_path, "w") as f:
        json.dump(default_content, f, indent=2)

print("Инициализация базы данных с реальными танками...")

# Создаем папки, если их нет
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(os.path.join(DATA_PATH, "images"), exist_ok=True)

# 1. Инициализация users.json
users_file = os.path.join(DATA_PATH, "users.json")
create_valid_json(users_file, {})

# 2. Инициализация promo_codes.json
promo_file = os.path.join(DATA_PATH, "promo_codes.json")
create_valid_json(promo_file, {})

# 3. Инициализация tanks.json
tanks_file = os.path.join(DATA_PATH, "tanks.json")
if not os.path.exists(tanks_file):
    # Создаем 3000 танков на основе реальных прототипов
    tanks = []
    rarity_distribution = ["Trash"]*500 + ["Common"]*700 + ["Uncommon"]*600 + ["Rare"]*500 + ["Epic"]*400 + ["Legendary"]*300
    
    # Создаем варианты реальных танков
    for i in range(3000):
        base_tank = random.choice(REAL_TANKS).copy()
        
        # Создаем уникальную модификацию
        variant_id = f"{base_tank['id']}-{i+1:04d}"
        variant_name = f"{base_tank['name']} M{random.randint(1, 10)}"
        
        # Модифицируем характеристики
        modified_tank = {
            "id": variant_id,
            "name": variant_name,
            "rarity": random.choice(rarity_distribution),
            "nation": base_tank["nation"],
            "type": base_tank["type"],
            "year": base_tank["year"] + random.randint(0, 10),
            "armor": self.modify_value(base_tank["armor"], 0.1) if isinstance(base_tank["armor"], int) else base_tank["armor"],
            "gun": f"{self.modify_value(float(base_tank['gun'].split()[0]), 0.15)} мм" if 'мм' in base_tank["gun"] else base_tank["gun"],
            "engine": f"{self.modify_value(float(base_tank['engine'].split()[0]), 0.2)} л.с." if 'л.с.' in base_tank["engine"] else base_tank["engine"],
            "speed": self.modify_value(base_tank["speed"], 0.15),
            "price": int(base_tank["price"] * random.uniform(0.8, 1.2)),
            "description": base_tank["description"]
        }
        tanks.append(modified_tank)
    
    with open(tanks_file, "w") as f:
        json.dump(tanks, f, indent=2)
    print(f"Создано {len(tanks)} модификаций реальных танков")
else:
    create_valid_json(tanks_file, [])

print("Инициализация базы данных завершена!")

def modify_value(base_value, variation):
    """Модифицирует базовое значение с вариацией ±variation%"""
    if isinstance(base_value, (int, float)):
        return int(base_value * random.uniform(1 - variation, 1 + variation))
    return base_value
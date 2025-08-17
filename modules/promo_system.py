import os
import json
import random
import string
from datetime import datetime, timedelta
from config import DATA_PATH

class PromoSystem:
    def __init__(self):
        self.data_file = os.path.join(DATA_PATH, "promo_codes.json")
        self.promos = self.load_promos()
    
    def load_promos(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        return {}
    
    def save_promos(self):
        with open(self.data_file, "w") as f:
            json.dump(self.promos, f, indent=2)
    
    def create_promo(self, reward, description, expires_days=30, max_uses=100):
        # Генерация кода
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        expires = (datetime.now() + timedelta(days=expires_days)).strftime("%Y-%m-%d %H:%M:%S")
        
        self.promos[code] = {
            "reward": reward,
            "description": description,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expires": expires,
            "max_uses": max_uses,
            "used_by": []
        }
        self.save_promos()
        return code
    
    def apply_promo(self, code, user_id):
        code = code.upper()
        if code in self.promos:
            promo = self.promos[code]
            # Проверка срока действия
            if datetime.strptime(promo["expires"], "%Y-%m-%d %H:%M:%S") < datetime.now():
                return False, "Промокод истек"
                
            # Проверка лимита
            if len(promo["used_by"]) >= promo["max_uses"]:
                return False, "Лимит использований исчерпан"
                
            # Проверка использования
            user_id = str(user_id)
            if user_id in promo["used_by"]:
                return False, "Вы уже использовали этот промокод"
                
            # Добавляем пользователя
            promo["used_by"].append(user_id)
            self.save_promos()
            return True, promo["description"]
        
        return False, "Неверный промокод"
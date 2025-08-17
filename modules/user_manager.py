import os
import json
import time
from config import DATA_PATH, CRATE_LIMIT, CRATE_PERIOD_HOURS

class UserManager:
    def __init__(self):
        self.data_file = os.path.join(DATA_PATH, "users.json")
        self.users = self.load_users()
    
    def load_users(self):
        # Создаем файл, если он не существует
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump({}, f)
            return {}
        
        # Проверяем, что файл не пустой
        if os.path.getsize(self.data_file) == 0:
            with open(self.data_file, "w") as f:
                json.dump({}, f)
            return {}
        
        # Читаем файл с обработкой ошибок
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Если файл поврежден, создаем новый
            with open(self.data_file, "w") as f:
                json.dump({}, f)
            return {}
    
    # Остальной код без изменений...
    def save_users(self):
        with open(self.data_file, "w") as f:
            json.dump(self.users, f, indent=2)
    
    # ... остальные методы без изменений
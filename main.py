import os
import time
import logging
import json
import random
from telebot import TeleBot, types

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "8399358948:AAEjSS7weboKJvoY5-6mGEy2Jd5K4OOmgQE"
ADMIN_IDS = [8316216845]
CRATE_LIMIT = 5
CRATE_PERIOD_HOURS = 5
DATA_PATH = "/storage/emulated/0/Documents/танк бот/data/"
ADMIN_SECRET = "Si900900"

# Инициализация бота
bot = TeleBot(BOT_TOKEN)

# Создаем папки для данных
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(os.path.join(DATA_PATH, "images"), exist_ok=True)

# Класс базы данных танков
class TankDatabase:
    def __init__(self):
        self.data_file = os.path.join(DATA_PATH, "tanks.json")
        self.tanks = self.load_tanks()
    
    def load_tanks(self):
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except:
            return []
    
    def get_tank(self, tank_id):
        for tank in self.tanks:
            if tank["id"] == tank_id:
                return tank
        return None
    
    def get_random_tank(self):
        return random.choice(self.tanks) if self.tanks else None

# Класс управления пользователями
class UserManager:
    def __init__(self):
        self.data_file = os.path.join(DATA_PATH, "users.json")
        self.users = self.load_users()
    
    def load_users(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump({}, f)
            return {}
        
        if os.path.getsize(self.data_file) == 0:
            with open(self.data_file, "w") as f:
                json.dump({}, f)
            return {}
        
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            with open(self.data_file, "w") as f:
                json.dump({}, f)
            return {}
    
    def save_users(self):
        with open(self.data_file, "w") as f:
            json.dump(self.users, f, indent=2)
    
    def add_user(self, user_id, username):
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = {
                "username": username,
                "collection": [],
                "opened_crates": 0,
                "last_crate_time": 0,
                "crates_today": 0,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.save_users()
            return True
        return False
    
    def can_open_crate(self, user_id):
        user_id = str(user_id)
        if user_id not in self.users:
            return False
            
        user = self.users[user_id]
        if time.time() - user["last_crate_time"] > CRATE_PERIOD_HOURS * 3600:
            user["crates_today"] = 0
            
        return user["crates_today"] < CRATE_LIMIT
    
    def add_tank_to_collection(self, user_id, tank_id):
        user_id = str(user_id)
        if user_id in self.users:
            if tank_id not in self.users[user_id]["collection"]:
                self.users[user_id]["collection"].append(tank_id)
                self.users[user_id]["opened_crates"] += 1
                self.users[user_id]["crates_today"] += 1
                self.users[user_id]["last_crate_time"] = time.time()
                self.save_users()
                return True
        return False
    
    def get_user_collection(self, user_id):
        user_id = str(user_id)
        return self.users.get(user_id, {}).get("collection", [])
    
    def reset_crate_limit(self, user_id):
        user_id = str(user_id)
        if user_id in self.users:
            self.users[user_id]["crates_today"] = 0
            self.users[user_id]["last_crate_time"] = 0
            self.save_users()
            return True
        return False

# Система кейсов
class CrateSystem:
    def __init__(self):
        self.tank_db = TankDatabase()
        
    def open_crate(self):
        tank = self.tank_db.get_random_tank()
        return tank if tank else None

# Просмотр коллекции
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
            return "🏆 Ваша коллекция пока пуста!"
            
        groups = {}
        for tank in self.get_collection_details(collection):
            rarity = tank["rarity"]
            groups.setdefault(rarity, []).append(tank)
        
        response = "🏆 Ваша коллекция танков:\n\n"
        for rarity, tanks in groups.items():
            response += f"⭐ {rarity} ({len(tanks)} танков):\n"
            for tank in tanks[:5]:
                response += f"  - {tank['name']}\n"
            if len(tanks) > 5:
                response += f"  ... и еще {len(tanks)-5}\n"
            response += "\n"
        
        return response

# Система промокодов
class PromoSystem:
    def __init__(self):
        self.data_file = os.path.join(DATA_PATH, "promo_codes.json")
        self.promos = self.load_promos()
    
    def load_promos(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_promos(self):
        with open(self.data_file, "w") as f:
            json.dump(self.promos, f, indent=2)
    
    def create_promo(self, reward, description, expires_days=30, max_uses=100):
        import string
        from datetime import datetime, timedelta
        
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
            from datetime import datetime
            if datetime.strptime(promo["expires"], "%Y-%m-%d %H:%M:%S") < datetime.now():
                return False, "Промокод истек"
                
            if len(promo["used_by"]) >= promo["max_uses"]:
                return False, "Лимит использований исчерпан"
                
            user_id = str(user_id)
            if user_id in promo["used_by"]:
                return False, "Вы уже использовали этот промокод"
                
            promo["used_by"].append(user_id)
            self.save_promos()
            return True, promo["description"]
        
        return False, "Неверный промокод"

# Админские функции
def is_admin(user_id):
    return user_id in ADMIN_IDS

def admin_panel_handler():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📊 Статистика", "🎁 Создать промокод")
    keyboard.add("👥 Список пользователей", "🔄 Сбросить лимиты")
    keyboard.add("❌ Закрыть панель")
    return "👑 Админ-панель управления\nВыберите действие:", keyboard

# Вспомогательные функции
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}ч {minutes}м"

def format_tank_info(tank):
    return (
        f"⚔️ {tank['name']} ({tank['year']})\n"
        f"🏷️ Редкость: {tank['rarity']}\n"
        f"🏳️ Нация: {tank['nation']}\n"
        f"🔰 Тип: {tank['type']}\n"
        f"🛡️ Броня: {tank['armor']}\n"
        f"🔫 Орудие: {tank['gun']}\n"
        f"🚀 Двигатель: {tank['engine']}\n"
        f"🏎️ Скорость: {tank['speed']} км/ч\n"
        f"📖 {tank['description']}"
    )

# Инициализация систем
try:
    user_manager = UserManager()
    crate_system = CrateSystem()
    collection_view = CollectionView()
    promo_system = PromoSystem()
    logger.info("Системы инициализированы успешно")
except Exception as e:
    logger.error(f"Ошибка инициализации систем: {e}")
    import setup_database
    setup_database
    user_manager = UserManager()
    crate_system = CrateSystem()
    collection_view = CollectionView()
    promo_system = PromoSystem()

# Обработчики команд
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or str(user_id)
    
    try:
        user_manager.add_user(user_id, username)
    except Exception as e:
        logger.error(f"Ошибка добавления пользователя: {e}")
        bot.reply_to(message, "❌ Произошла ошибка при регистрации. Попробуйте позже.")
        return
    
    if is_admin(user_id):
        text = (
            "👑 Добро пожаловать, Администратор!\n"
            f"Используйте /{ADMIN_SECRET} для доступа к панели управления\n\n"
            "⚙️ Доступные команды:\n"
            "/open_crate - Открыть кейс\n"
            "/mycollection - Ваша коллекция\n"
            "/stats - Статистика бота"
        )
    else:
        text = (
            "🎮 Добро пожаловать в Танковую Коллекцию!\n\n"
            "⚡ Каждые 5 часов вы можете открыть до 5 кейсов с реальными историческими танками!\n\n"
            "⚙️ Доступные команды:\n"
            "/open_crate - Открыть кейс\n"
            "/mycollection - Ваша коллекция\n"
            "/promo [код] - Активировать промокод"
        )
    
    bot.reply_to(message, text)

@bot.message_handler(commands=['open_crate'])
def open_crate(message):
    user_id = message.from_user.id
    
    try:
        can_open = user_manager.can_open_crate(user_id)
    except Exception as e:
        logger.error(f"Ошибка проверки лимита кейсов: {e}")
        bot.reply_to(message, "❌ Произошла ошибка. Попробуйте позже.")
        return
    
    if not can_open:
        try:
            user_data = user_manager.users.get(str(user_id), {})
            last_time = user_data.get("last_crate_time", 0)
            next_time = last_time + CRATE_PERIOD_HOURS * 3600
            wait_time = max(0, next_time - time.time())
            
            bot.reply_to(
                message,
                f"⏳ Вы исчерпали лимит кейсов!\n"
                f"Следующее открытие через: {format_time(wait_time)}"
            )
        except Exception as e:
            logger.error(f"Ошибка расчета времени: {e}")
            bot.reply_to(message, "⏳ Вы исчерпали лимит кейсов! Попробуйте позже.")
        return
    
    try:
        tank = crate_system.open_crate()
    except Exception as e:
        logger.error(f"Ошибка открытия кейса: {e}")
        bot.reply_to(message, "❌ Ошибка при открытии кейса")
        return
    
    if tank:
        try:
            if user_manager.add_tank_to_collection(user_id, tank["id"]):
                response = (
                    f"🎉 Поздравляем! Вы получили реальный танк:\n\n"
                    f"{format_tank_info(tank)}"
                )
                bot.reply_to(message, response)
                return
        except Exception as e:
            logger.error(f"Ошибка добавления танка: {e}")
    
    bot.reply_to(message, "❌ Ошибка при открытии кейса")

@bot.message_handler(commands=['mycollection'])
def show_collection(message):
    user_id = message.from_user.id
    try:
        collection = user_manager.get_user_collection(user_id)
        response = collection_view.format_collection(collection)
        bot.reply_to(message, response)
    except Exception as e:
        logger.error(f"Ошибка показа коллекции: {e}")
        bot.reply_to(message, "❌ Ошибка при загрузке коллекции")

@bot.message_handler(commands=['promo'])
def apply_promo(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) < 2:
        bot.reply_to(message, "ℹ️ Укажите промокод: /promo КОД")
        return
    
    promo_code = args[1]
    try:
        success, result = promo_system.apply_promo(promo_code, user_id)
    except Exception as e:
        logger.error(f"Ошибка применения промокода: {e}")
        bot.reply_to(message, "❌ Ошибка при обработке промокода")
        return
    
    if success:
        try:
            user_manager.reset_crate_limit(user_id)
            bot.reply_to(message, f"🎉 Промокод активирован!\n{result}")
        except Exception as e:
            logger.error(f"Ошибка сброса лимита: {e}")
            bot.reply_to(message, f"🎉 Промокод активирован, но сброс лимита не удался")
    else:
        bot.reply_to(message, f"❌ {result}")

@bot.message_handler(commands=[ADMIN_SECRET])
def admin_command(message):
    if is_admin(message.from_user.id):
        try:
            text, keyboard = admin_panel_handler()
            bot.send_message(message.chat.id, text, reply_markup=keyboard)
        except Exception as e:
            logger.error(f"Ошибка админ-панели: {e}")
            bot.reply_to(message, "❌ Ошибка при открытии админ-панели")
    else:
        bot.reply_to(message, "⛔ Доступ запрещен")

@bot.message_handler(func=lambda msg: msg.text == "❌ Закрыть панель")
def close_admin_panel(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "Админ-панель закрыта", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.reply_to(message, "⛔ Доступ запрещен")

@bot.message_handler(func=lambda msg: msg.text == "📊 Статистика")
def show_stats(message):
    if is_admin(message.from_user.id):
        try:
            total_users = len(user_manager.users)
            total_tanks = sum(len(user['collection']) for user in user_manager.users.values())
            bot.reply_to(message, f"📊 Статистика бота:\n\n👥 Пользователей: {total_users}\n🎁 Открыто кейсов: {total_tanks}")
        except Exception as e:
            logger.error(f"Ошибка статистики: {e}")
            bot.reply_to(message, "❌ Ошибка при получении статистики")

@bot.message_handler(func=lambda msg: msg.text == "🎁 Создать промокод")
def create_promo(message):
    if is_admin(message.from_user.id):
        try:
            code = promo_system.create_promo(
                reward="Сброс лимита кейсов",
                description="Позволяет сбросить лимит открытия кейсов",
                expires_days=30,
                max_uses=100
            )
            bot.reply_to(message, f"✅ Создан промокод: {code}\nНаграда: Сброс лимита кейсов")
        except Exception as e:
            logger.error(f"Ошибка создания промокода: {e}")
            bot.reply_to(message, "❌ Ошибка при создании промокода")

@bot.message_handler(func=lambda msg: msg.text == "👥 Список пользователей")
def user_list(message):
    if is_admin(message.from_user.id):
        try:
            users = user_manager.users
            response = "👥 Пользователи бота:\n\n"
            for user_id, data in users.items():
                response += f"👤 {data['username']} (ID: {user_id})\n"
                response += f"🎁 Открыто кейсов: {data['opened_crates']}\n\n"
            bot.reply_to(message, response)
        except Exception as e:
            logger.error(f"Ошибка списка пользователей: {e}")
            bot.reply_to(message, "❌ Ошибка при загрузке списка пользователей")

@bot.message_handler(func=lambda msg: msg.text == "🔄 Сбросить лимиты")
def reset_limits(message):
    if is_admin(message.from_user.id):
        try:
            for user_id in user_manager.users:
                user_manager.reset_crate_limit(user_id)
            bot.reply_to(message, "✅ Лимиты всех пользователей сброшены!")
        except Exception as e:
            logger.error(f"Ошибка сброса лимитов: {e}")
            bot.reply_to(message, "❌ Ошибка при сбросе лимитов")

# Запуск бота
if __name__ == '__main__':
    logger.info("Бот запускается...")
    logger.info(f"Токен бота: {BOT_TOKEN}")
    logger.info(f"ID администратора: {ADMIN_IDS}")
    
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

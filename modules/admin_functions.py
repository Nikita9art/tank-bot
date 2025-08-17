from telebot import types
from config import ADMIN_IDS

def is_admin(user_id):
    return user_id in ADMIN_IDS

def admin_panel_handler():
    # Создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📊 Статистика", "🎁 Создать промокод")
    keyboard.add("👥 Список пользователей", "🔄 Сбросить лимиты")
    keyboard.add("❌ Закрыть панель")
    
    return "👑 Админ-панель управления\nВыберите действие:", keyboard
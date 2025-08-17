import time
from datetime import datetime

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}ч {minutes}м"

def format_tank_info(tank):
    return (
        f"⚔️ {tank['name']}\n"
        f"🏷️ Редкость: {tank['rarity']}\n"
        f"🏳️ Нация: {tank['nation']}\n"
        f"💵 Цена: ${tank['price']:,}\n"
        f"🛡️ Броня: {tank['armor']} мм\n"
        f"🔫 Орудие: {tank['gun']}\n"
        f"🏎️ Скорость: {tank['speed']} км/ч"
    )
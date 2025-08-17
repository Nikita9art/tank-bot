from PIL import Image, ImageDraw, ImageFont
import random
import os
from config import DATA_PATH

def generate_tank_image(tank_id, tank_name):
    # Создаем изображение
    img = Image.new('RGB', (300, 200), color=(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)))
    d = ImageDraw.Draw(img)
    
    # Рисуем корпус танка
    d.rectangle([50, 100, 250, 150], fill=(100, 100, 100))
    
    # Рисуем башню
    d.rectangle([100, 70, 200, 100], fill=(120, 120, 120))
    
    # Рисуем пушку
    d.rectangle([140, 50, 160, 70], fill=(80, 80, 80))
    
    # Добавляем текст
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = None
        
    d.text((20, 20), tank_name, fill=(255, 255, 255), font=font)
    
    # Сохраняем изображение
    os.makedirs(os.path.join(DATA_PATH, "images"), exist_ok=True)
    img_path = os.path.join(DATA_PATH, "images", f"tank_{tank_id}.jpg")
    img.save(img_path)
    return img_path
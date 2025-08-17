#!/data/data/com.termux/files/usr/bin/bash

cd "/storage/emulated/0/Documents/танк бот"

echo "Обновление Termux и установка зависимостей..."
pkg update -y
pkg install -y python libjpeg-turbo
pip install --upgrade pip wheel

echo "Установка зависимостей Python..."
LDFLAGS="-L/system/lib64" CFLAGS="-I/data/data/com.termux/files/usr/include" pip install pyTelegramBotAPI Pillow

echo "Инициализация базы данных..."
python setup_database.py

echo "Проверка файлов данных..."
ls -l data/

echo "Запуск бота..."
python main.py

#!/bin/bash

# Завантажує змінні оточення з файлу .env
set -o allexport
source .env
set +o allexport

# Зупиняємо поточний процес бота
pkill -f bot.py

# Запускаємо новий процес бота
nohup python3 bot.py &
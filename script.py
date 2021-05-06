"""
Скрипт для форматирования данных из файла data.py в json-файл
"""
import json
import data

my_data = []
my_data.append(data.goals)
my_data.append(data.teachers)

with open('db.json', 'w', encoding='utf-8') as f:
    json.dump(my_data, f)


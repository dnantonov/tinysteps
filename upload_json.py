"""
Скрипт для добавления в БД данных о преподавателях из db.json
"""

import json
from app import Teacher, app, db, migrate


with open("db.json", "r", encoding='utf-8') as f:
    goals, teachers = json.load(f)
    for teacher in teachers:
        db.session.add(Teacher(name=teacher['name'], about=teacher['about'], rating=teacher['rating'],
                               picture=teacher['picture'], price=teacher['price'], goals=str(teacher['goals']),
                               free=str(teacher['free'])))

db.session.commit()
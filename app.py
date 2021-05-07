import json
from flask import Flask, render_template, request, redirect, url_for
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField


app = Flask(__name__)
app.secret_key = "my_super_secret_key"

WEEKDAYS = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресенье'
}

ICONS = {
    'travel': '⛱',
    'relocate': '🚜',
    'study': '🏫',
    'work': '🏢'
}


class BookingForm(FlaskForm):
    name = StringField("Вас зовут", [InputRequired()])
    phone = StringField("Ваш телефон", [InputRequired()])


class RequestForm(FlaskForm):
    name = StringField("Вас зовут", [InputRequired()])
    phone = StringField("Ваш телефон", [InputRequired()])
    goal = RadioField(
        'Какая цель занятий?',
        choices=[('Для путешествий', 'Для путешествий'), ('Для школы', 'Для школы'),
                 ('Для работы', 'Для работы'), ('Для переезда', 'Для переезда')]
    )
    time = RadioField(
        'Сколько времени есть?',
        choices=[('1-2 часа в неделю', '1-2 часа в неделю'), ('3-5 часов в неделю', '3-5 часов в неделю'),
                 ('5-7 часов в неделю', '5-7 часов в неделю'), ('7-10 часов в неделю', '7-10 часов в неделю')]
    )


with open("db.json", "r", encoding='utf-8') as f:
    goals, teachers = json.load(f)


@app.route('/')
def index():
    """
    Функция отображения главной страницы
    """
    return render_template('index.html')


@app.route('/all')
def all_teachers():
    """
    Функция отображения страницы со всеми преподавателями
    """
    return render_template('all.html')


@app.route('/goals/<goal>/')
def teachers_by_goal(goal):
    """
    Функция отображения целей
    """
    teachers_goal = []
    # фильтруем преподавателей по целям обучения, добавляем их в новый список
    for teacher in teachers:
        if goal in teacher['goals']:
            teachers_goal.append(teacher)
    # сортируем список преодавателей по рейтингу
    sorted_teachers = sorted(teachers_goal, key=lambda k: k['rating'])[::-1]
    # определяем иконку для цели и достаем название цели из словаря
    icon = ICONS[goal]
    goal = goals[goal]
    return render_template('goal.html', goal=goal, icon=icon, teachers=sorted_teachers)


@app.route('/profiles/<int:teacher_id>/')
def teacher_profile(teacher_id):
    """
    Функция отображения страницы профиля преподавателя
    """
    teacher = teachers[teacher_id]
    teacher_goals = [goals[x] for x in teacher["goals"]]
    days = teacher["free"]
    # проверка в каких днях нет свободных мест
    free_days = {}
    for day in days.keys():
        free_days[day] = all(x is False for x in teacher["free"][day].values())
    return render_template('profile.html', teacher=teacher, goals=teacher_goals,
                           days=days, free_days=free_days)


@app.route('/request/')
def request_select():
    """
    Функция отображения формы-заявки на консультацию
    """
    form = RequestForm()
    return render_template('request.html', form=form)


@app.route('/request_done/', methods=['GET', 'POST'])
def request_done():
    """
    Функция отображения заявки на консультацию и сохранение данных в json
    """
    if request.method == 'POST':
        goal = request.form.get('goal')
        time = request.form.get('time')
        name = request.form.get('name')
        phone = request.form.get('phone')
        data = {"goal": goal, "time": time, "name": name, "phone": phone}
        with open("request.json", "a", encoding='utf-8') as db:
            json.dump(data, db, indent=4)
        return render_template('request_done.html', goal=goal, time=time,
                               name=name, phone=phone)


@app.route('/booking/<int:teacher_id>/<day>/<time>/')
def booking_teacher(teacher_id, day, time):
    """
    Функция отображения формы-заявки на обучение
    """
    form = BookingForm()
    selected_day = WEEKDAYS[day]
    teacher = teachers[teacher_id]
    return render_template('booking.html', teacher_id=teacher_id, day=day, full_day=selected_day,
                           time=time, teacher=teacher, form=form)


@app.route('/booking_done/', methods=['GET', 'POST'])
def booking_done():
    """
    Функция отображения успешной заявки формы и сохранение данных в json
    """
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        day = WEEKDAYS[request.form.get('clientWeekday')]
        time = request.form.get('clientTime')
        data = {'name': name, 'phone': phone, 'day': day, 'time': time}
        with open("booking.json", "a", encoding='utf-8') as db:
            json.dump(data, db, indent=4)
        return render_template('booking_done.html', name=name, phone=phone, day=day, time=time)
    else:
        return render_template('booking.html')


app.run(port=5000, debug=True)

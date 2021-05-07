import json
from flask import Flask, render_template, request, redirect, url_for
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField


app = Flask(__name__)
app.secret_key = "my_super_secret_key"

day_of_week = {
        'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed': 'Среда',
        'thu': 'Четверг',
        'fri': 'Пятница',
        'sat': 'Суббота',
        'sun': 'Воскресенье'
}

goals_dict = {
    'travel': 'Для путешествий',
    'learn': 'Для школы',
    'work': 'Для работы',
    'move': 'Для переезда'
}


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
def select_goal(goal):
    """
    Функция отображения целейй
    """
    return render_template('goal.html')


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
    return render_template('request.html')


@app.route('/request_done/', methods=['GET', 'POST'])
def request_done():
    if request.method == 'POST':
        goal_code = request.form.get('goal')
        goal = goals_dict[goal_code]
        time = request.form.get('time')
        name = request.form.get('name')
        phone = request.form.get('phone')
        return render_template('request_done.html', goal=goal, time=time,
                               name=name, phone=phone)


@app.route('/booking/<int:teacher_id>/<day>/<time>/')
def booking_teacher(teacher_id, day, time):
    """
    Функция отображения формы-заявки на обучение
    """
    selected_day = day_of_week[day]
    teacher = teachers[teacher_id]
    return render_template('booking.html', teacher_id=teacher_id, day=day, full_day=selected_day,
                           time=time, teacher=teacher)


@app.route('/booking_done/', methods=['GET', 'POST'])
def booking_done():
    """
    Функция отображения успешной заявки формы и сохранение данных в json
    """
    if request.method == 'POST':
        name = request.form.get('clientName')
        phone = request.form.get('clientPhone')
        day = day_of_week[request.form.get('clientWeekday')]
        time = request.form.get('clientTime')
        data = {'name': name, 'phone': phone, 'day': day, 'time': time}
        with open("booking.json", "a", encoding='utf-8') as db:
            json.dump(data, db, indent=4)
        return render_template('booking_done.html', name=name, phone=phone, day=day, time=time)
    else:
        return render_template('booking.html')


app.run(port=5000, debug=True)
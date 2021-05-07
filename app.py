import json
from flask import Flask, render_template, request, redirect, url_for
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm
from wtforms import StringField


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

with open("db.json", "r", encoding='utf-8') as f:
    goals, teachers = json.load(f)


class MyForm(FlaskForm):
    name = StringField('Имя', [InputRequired()])
    phone = StringField('Ваш телефон', [Length(min=5, max=12)])


@app.route('/')
def index():
    return "Здесь будет главная"


@app.route('/all')
def all_teachers():
    return "Здесь будут преподаватели"


@app.route('/goals/<goal>/')
def select_goal(goal):
    return "Здесь будет цель <goal>"


@app.route('/profiles/<int:teacher_id>/')
def teacher_profile(teacher_id):
    teacher = teachers[teacher_id]
    teacher_goals = [goals[x] for x in teacher["goals"]]
    days = teacher["free"]
    # проверка в каких днях нет свободных мест
    free_days = {}
    for day in days.keys():
        free_days[day] = all(x is False for x in teacher["free"][day].values())
    return render_template('profile.html',
                           teacher=teacher,
                           goals=teacher_goals,
                           days=days,
                           free_days=free_days)


@app.route('/request/')
def request_select():
    return "Здесь будет заявка на подбор"


@app.route('/request_done/')
def request_done():
    return "Заявка на подбор отправлена"


@app.route('/booking/<int:teacher_id>/<day>/<time>/')
def booking_teacher(teacher_id, day, time):
    form = MyForm()
    selected_day = day_of_week[day]
    teacher = teachers[teacher_id]
    return render_template('booking.html',
                           teacher_id=teacher_id,
                           day=day,
                           full_day=selected_day,
                           time=time,
                           teacher=teacher,
                           form=form)


@app.route('/booking_done/', methods=['GET', 'POST'])
def booking_done():
    if request.method == 'POST':
        name = request.form.get('clientName')
        phone = request.form.get('clientPhone')
        day = day_of_week[request.form.get('clientWeekday')]
        time = request.form.get('clientTime')
        data = {'name': name, 'phone': phone, 'day': day, 'time': time}

        with open("booking.json", "a", encoding='utf-8') as db:
            json.dump(data, db, indent=4)
        return render_template('booking_done.html',
                               name=name,
                               phone=phone,
                               day=day,
                               time=time)


app.run(port=5000, debug=True)
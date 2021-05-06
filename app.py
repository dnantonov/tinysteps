import json

from flask import Flask, request, render_template
from wtforms.validators import InputRequired, Email
from flask_wtf import FlaskForm
from wtforms import StringField


app = Flask(__name__)
app.secret_key = "randomstring"

with open("db.json", "r", encoding='utf-8') as f:
    goals, teachers = json.load(f)

class MyForm(FlaskForm):
    name = StringField('name', [InputRequired()])
    mail = StringField('mail', [Email()])


@app.route('/')
def render_index():
    form = MyForm()
    return render_template("form.html", form=form)


@app.route('/send/', methods=["POST"])
def render_send():
    form = MyForm()
    if form.validate():
        return "Форма в порядке"
    else:
        return "Форма не в порядке"

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
        free_days[day] = all(x == False for x in teacher["free"][day].values())
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
    return "здесь будет форма бронирования <teacher_id>"

@app.route('/booking_done/')
def booking_done():
    return "заявка отправлена"


app.run(port=5000, debug=True)
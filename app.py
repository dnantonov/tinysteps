from flask import Flask, request, render_template
from wtforms.validators import InputRequired, Email
from flask_wtf import FlaskForm
from wtforms import StringField


app = Flask(__name__)
app.secret_key = "randomstring"

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
        return "Форма в порядке"return "Форма не в порядке"

@app.route('/')
def index():
    return "Здесь будет главная"

@app.route('/all')
def all_teachers():
    return "Здесь будут преподаватели"

@app.route('/goals/<goal>/')
def goals(goal):
    return "Здесь будет цель <goal>"

@app.route('/profiles/<int:teacher_id>/')
def teacher_profile(teacher_id):
    return "Здесь будет преподаватель <teacher_id>"

@app.route('/request/')
def request_select():
    return "Здесь будет заявка на подбор"

@app.route('/request_done/')
def request_done():
    return "Заявка на подбор отправлена"

@app.route('/booking/<int:teacher_id>/<str:day>/<str:time>/')
def booking_teacher(teacher_id, day, time):
    return "здесь будет форма бронирования <teacher_id>"

@app.route('/booking_done/')
def booking_done():
    return "заявка отправлена"


app.run(port=8060, debug=True)
import json
import os
import random
from collections import OrderedDict

from flask import Flask, render_template, request, redirect, url_for
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


WEEKDAYS = OrderedDict({
    "mon": {"short_ver": "Пн",
            "full_ver": "Понедельник"},
    "tue": {"short_ver": "Вт",
            "full_ver": "Вторник"},
    "wed": {"short_ver": "Ср",
            "full_ver": "Среда"},
    "thu": {"short_ver": "Чт",
            "full_ver": "Четверг"},
    "fri": {"short_ver": "Пт",
            "full_ver": "Пятница"},
    "sat": {"short_ver": "Сб",
            "full_ver": "Суббота"},
    "sun": {"short_ver": "Вс",
            "full_ver": "Воскресенье"}
})

GOALS = OrderedDict({
    "travel": {"desc": "для путешествий", "icon": "⛱"},
    "study": {"desc": "для учебы", "icon": "🏫"},
    "work": {"desc": "для работы", "icon": "🏢"},
    "relocate": {"desc": "для переезда", "icon": "🚜"},
    "coding": {"desc": "для программирования", "icon": "💻"}
})


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    about = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float)
    picture = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.String, nullable=False)
    free = db.Column(db.String, nullable=False)
    bookings = db.relationship('Booking',  back_populates="teacher")

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    day = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(15), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship('Teacher', back_populates="bookings")

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    goal = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(15), nullable=False)

db.create_all()


class BookingForm(FlaskForm):
    name = StringField("Вас зовут", validators=[InputRequired()])
    phone = StringField("Ваш телефон", validators=[InputRequired()])


class RequestForm(FlaskForm):
    name = StringField("Вас зовут", validators=[InputRequired()])
    phone = StringField("Ваш телефон", validators=[InputRequired()])
    goal = RadioField(
        'Какая цель занятий?', validators=[InputRequired()],
        choices=[('Для путешествий', 'Для путешествий'), ('Для школы', 'Для школы'),
                 ('Для работы', 'Для работы'), ('Для переезда', 'Для переезда')]
    )
    time = RadioField(
        'Сколько времени есть?', validators=[InputRequired()],
        choices=[('1-2 часа в неделю', '1-2 часа в неделю'), ('3-5 часов в неделю', '3-5 часов в неделю'),
                 ('5-7 часов в неделю', '5-7 часов в неделю'), ('7-10 часов в неделю', '7-10 часов в неделю')]
    )


@app.route('/')
def index():
    """
    Функция отображения главной страницы
    """
    # делаем запрос к БД, получаем всех учитилей и перемешиваем их, чтобы получить случайных преподавателей
    teachers = db.session.query(Teacher).all()
    random.shuffle(teachers)
    return render_template('index.html', teachers=teachers[:6])


@app.route('/all/', methods=['GET', 'POST'])
def all_teachers():
    """
    Функция отображения страницы со всеми преподавателями
    """
    sort = request.form.get('sort')
    if sort == "random":
        teachers = db.session.query(Teacher).all()
        random.shuffle(teachers)
    elif sort == "rating":
        teachers = db.session.query(Teacher).order_by(Teacher.rating.desc())
    elif sort == "expensive":
        teachers = db.session.query(Teacher).order_by(Teacher.price.desc())
    elif sort == "cheap":
        teachers = db.session.query(Teacher).order_by(Teacher.price)
    else:
        teachers = db.session.query(Teacher).all()
    teachers_quantity = db.session.query(Teacher).count()
    return render_template('all.html', teachers=teachers, teachers_quantity=teachers_quantity, sort=sort)


@app.route('/goals/<goal>/')
def teachers_by_goal(goal):
    """
    Функция отображения целей
    """
    # делаем запрос к БД, достаем преподавателей с нашей целью и сортируем по рейтингу
    query = Teacher.query.filter(Teacher.goals.contains(goal))
    teachers = query.order_by(Teacher.rating.desc()).all()
    # определяем иконку для цели и достаем название цели из словаря
    goal = GOALS[goal]
    return render_template('goal.html', goal=goal, teachers=teachers)


@app.route('/profiles/<int:teacher_id>/')
def teacher_profile(teacher_id):
    """
    Функция отображения страницы профиля преподавателя
    """
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    teacher_goals = [GOALS[x] for x in eval(teacher.goals)] # получаем список целей учителя по коду цели
    days = eval(teacher.free) # преобазуем свободные даты для занятий из строки в словарь
    # проверка в каких днях нет свободных мест
    free_days = {}
    for day in days.keys():
        free_days[day] = all(x is False for x in days[day].values())
    return render_template('profile.html', teacher=teacher,
                           goals=teacher_goals, days=days,
                           free_days=free_days)


@app.route('/request/', methods=['GET', 'POST'])
def request_select():
    """
    Функция отображения формы-заявки на консультацию
    """
    form = RequestForm()
    if request.method == 'POST':
        goal = request.form.get('goal')
        time = request.form.get('time')
        name = request.form.get('name')
        phone = request.form.get('phone')
        req = Request(name=name, phone=phone, goal=goal, time=time)
        db.session.add(req)
        db.session.commit()
        return render_template('request_done.html', goal=goal, time=time,
                               name=name, phone=phone)
    else:
        return render_template('request.html', form=form)


@app.route('/booking/<int:teacher_id>/<day>/<time>/', methods=['GET', 'POST'])
def booking_teacher(teacher_id, day, time):
    """
    Функция отображения формы-заявки на обучение
    """
    form = BookingForm()
    selected_day = WEEKDAYS[day]
    teacher = db.session.query(Teacher).get(teacher_id)
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        day = WEEKDAYS[request.form.get('clientWeekday')]
        time = request.form.get('clientTime')
        booking = Booking(name=name, phone=phone, day=day['full_ver'], time=time, teacher=teacher)
        db.session.add(booking)
        db.session.commit()
        return render_template('booking_done.html', name=name,
                               phone=phone, day=day, time=time)
    else:
        return render_template('booking.html', teacher_id=teacher_id,
                               day=day, selected_day=selected_day,
                               time=time, teacher=teacher, form=form)


if __name__ == '__main__':
    app.run(port=5000, debug=True)

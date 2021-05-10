from collections import defaultdict, OrderedDict

days_of_week = OrderedDict({
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

goals = OrderedDict({
    "travel": {"desc": "для путешествий", "icon": "⛱"},
    "study": {"desc": "для учебы", "icon": "🏫"},
    "work": {"desc": "для работы", "icon": "🏢"},
    "relocate": {"desc": "для переезда", "icon": "🚜"}
})
from flask import Blueprint

reservations = Blueprint('reservations', __name__)

from . import controllers
# Маршруты приложения хранятся в модуле app/main/controllers.py
# внутри пакета, а обработчики ошибок – в модуле app/main/errors.py.
# Импортирование этих модулей связывает маршруты и обработчики с макетом.
# Важно отметить, что модули импортируются внизу сценария app/__init__.py, чтобы избежать циклических зависимостей, так
# как controllers.py и errors.py должны импортировать главный макет
from flask import Flask, render_template
from env_settings import secret_key
from user.routers import user_router
from flask_login import LoginManager
from database.connect_database import session_maker
from database.models import User
from account.routers import account_router
from settings_cached import cache
from transactions.routers import transactions_route
from analytics.routers import analytics_routes
from user.user_settings_routes import user_settings_routes
from errors.error_handlers import page_not_found, interval_error_server, handle_exception

app = Flask(__name__)

# подключение кэширование
cache.init_app(app)

app.secret_key = secret_key
app.register_blueprint(user_router)
app.register_blueprint(account_router)
app.register_blueprint(transactions_route)
app.register_blueprint(analytics_routes)
app.register_blueprint(user_settings_routes)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, interval_error_server)
app.register_error_handler(500, handle_exception)

# настройки для flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_router.user_login"
login_manager.login_message = "you need to log in"
login_manager.login_message_category = "info"


@app.template_filter('format_time')
def format_time(value):
    """
    Фильтр для форматирования времени
    :param value: значение времени, которое необходимо отформатировать
    :return: отформатированную строку времени в виде (день-месяц-год(полностью) часы:минуты)
    """

    return value.strftime('%d-%m-%Y %H:%M')


@app.get("/")
def index():
    """
    Главная страница
    :return: рендарит шаблон для главной странице
    """
    response = {
        "title": "Портала для управления финансами"
    }
    return render_template("index.html", response=response)


@login_manager.user_loader
def load_user(user_id):
    """
    Получение пользователя из базы данных
    :param user_id: id пользователя
    :return: либо вернет None, либо вернет пользователя
    """

    with session_maker() as db_session:
        return db_session.get(User, int(user_id))

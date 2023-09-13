from flask import Flask, render_template
from env_settings import secret_key
from user.routers import user_router
from flask_login import LoginManager
from database.connect_database import session_maker
from database.models import User
from account.routers import account_router
from settings_cached import cache

app = Flask(__name__)

# подключение кэширование
cache.init_app(app)

app.secret_key = secret_key
app.register_blueprint(user_router)
app.register_blueprint(account_router)

# настройки для flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_router.user_login"
login_manager.login_message = "you need to log in"
login_manager.login_message_category = "info"


@app.get("/")
def index():
    """
    Главная страница
    :return: рендарит шаблон для главной странице
    """

    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    """
    Получение пользователя из базы данных
    :param user_id: id пользователя
    :return: либо вернет None, либо вернет пользователя
    """

    with session_maker() as db_session:
        return db_session.get(User, int(user_id))

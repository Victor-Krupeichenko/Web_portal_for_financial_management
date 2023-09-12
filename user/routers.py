from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from user.forms import RegisterUserForm, UserLogin
from utils import form_field_pop, create_record__database, get_errors_field
from database.models import User
from passlib.hash import pbkdf2_sha256
from flask_login import login_user, login_required, current_user, logout_user

user_router = Blueprint("user_router", __name__, template_folder="templates", static_folder="static")


@user_router.route("/user-register", methods=["GET", "POST"])
def register_user():
    """
    Регистрация пользователя(создания записи в таблице user)
    - в случае успешной регистрации авторизует пользователя
    """
    form = RegisterUserForm()
    response = {
        "title": "User Register",
        "register": True
    }
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = form_field_pop(form, "csrf_token", "confirm_password")
            form_data["password"] = pbkdf2_sha256.hash(form_data.get("password"))
            record = create_record__database(User, form_data)
            if record is not None:
                login_user(record)
                # устанавливаем сеанс с постоянным временем жизни
                # (даже если закроем бравзер пользователь останется авторизованным)
                session.permanent = True
                return redirect(url_for("index"))
        else:
            get_errors_field(form)
    return render_template("user/user_template.html", response=response, form=form)


@user_router.route("/user-logout")
@login_required
def user_logout():
    """
    Выход пользователя
    """

    name = current_user.username
    logout_user()
    flash(message=f"User: {name} came out", category="info")
    return redirect(url_for("index"))


@user_router.route("/user-login", methods=["GET", "POST"])
def user_login():
    """
    Авторизация пользователя
    """

    form = UserLogin()
    response = {
        "title": "User Login",
        "login": True
    }
    if request.method == "POST":
        if form.validate_on_submit():
            flash(message=f"User: {form.data.get('username')} authorized", category="success")
            return redirect(url_for("index"))
        get_errors_field(form)
    return render_template("user/user_template.html", response=response, form=form)

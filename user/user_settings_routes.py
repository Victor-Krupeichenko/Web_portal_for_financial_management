from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from user.forms import PasswordChangeForm
from utils import get_errors_field, apply_changes, delete_object
from passlib.hash import pbkdf2_sha256
from database.models import User

user_settings_routes = Blueprint(
    "user_settings_routes", __name__, template_folder="templates", static_folder="static"
)


@user_settings_routes.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """
    Смена пароля
    """

    form = PasswordChangeForm()
    response = {
        "title": f"Change Password {current_user.username}",
        "change_password": True
    }
    if request.method == "POST":
        if form.validate_on_submit():
            new_password = pbkdf2_sha256.hash(form.data.get("new_password"))
            current_user.password = new_password
            apply_changes(current_user)
            logout_user()
            flash(message="password changed successfully", category="info")
            return redirect(url_for("user_router.user_login"))
        get_errors_field(form)
    return render_template("user/user_template.html", form=form, response=response)


@user_settings_routes.route("/user-delete")
@login_required
def delete_user():
    """
    Удаляет пользователя
    """

    user_id = current_user.id
    logout_user()
    delete_object(User, user_id)
    return redirect(url_for("user_router.register_user"))

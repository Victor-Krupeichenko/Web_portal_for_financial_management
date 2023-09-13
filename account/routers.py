from flask import Blueprint, request, render_template, redirect, url_for, flash
from account.forms import CreateAccountForm
from flask_login import login_required, current_user
from utils import (
    form_field_pop, get_errors_field, create_record_database, get_list_object, get_object, apply_changes, delete_object
)
from database.models import Account
from settings_cached import cache

account_router = Blueprint("account_router", __name__, template_folder="templates", static_folder="static")


@account_router.route("/account-create", methods=["GET", "POST"])
@login_required
def account_create():
    """
    Создание нового счета
    """

    form = CreateAccountForm()
    response = {
        "title": "Create Account",
        "acount_create": True
    }
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = form_field_pop(form, "csrf_token")
            form_data.setdefault("user_id", current_user.id)
            record = create_record_database(Account, form_data)
            if record is not None:
                flash(message=f"account: {form_data.get('name')} created successfully", category="success")
                return redirect(url_for("index"))
        get_errors_field(form)

    return render_template("account/account_template.html", response=response, form=form)


@account_router.get("/account-list")
@login_required
@cache.cached(timeout=60, key_prefix=lambda: str(current_user.id))
def get_list_accounts():
    """
    Просмотр списка счетов
    """

    response = {
        "title": f"Accounts {current_user.username}",
        "account_list": True
    }
    results = get_list_object(Account, current_user.id)
    if results is not None:
        return render_template("account/account_list.html", response=response, results=results)


@account_router.route("/account-edit/<int:account_id>/", methods=["GET", "POST"])
@login_required
def edit_account(account_id):
    """
    Обновление счета
    :param account_id: id аккаунта
    """

    form = CreateAccountForm()
    result = get_object(Account, account_id)
    if not result:
        return redirect(url_for("account_router.get_list_accounts"))
    response = {
        "title": f"Edit Account: {result.name}",
        "account_edit": True
    }
    if request.method == "POST":
        if form.validate_on_submit():
            result.name = form.data.get("name")
            result.balance = form.data.get("balance")
            apply_changes(result)
            return redirect(url_for("account_router.get_list_accounts"))
        get_errors_field(form)
    return render_template(
        "account/account_template.html", response=response, form=form, result=result,
    )


@account_router.route("/account-delete/<int:account_id>")
@login_required
def delete_account(account_id):
    """
    Удаление счета
    :param account_id: id account
    """

    delete_object(Account, account_id)
    return redirect(url_for("index"))

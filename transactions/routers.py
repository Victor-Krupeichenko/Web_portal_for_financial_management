from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from transactions.forms import CreateTransactionsForm
from utils import (
    get_object, form_field_pop, create_transaction_and_update_account, adding_required_fields_to_form, get_errors_field,
    delete_object, get_all_list_transaction_to_account, get_list_object
)
from database.models import Account, Transaction

transactions_route = Blueprint(
    "transactions_route", __name__, template_folder="templates", static_folder="static"
)


@transactions_route.route("/transactions-consuption/<int:account_id>", methods=["GET", "POST"])
@login_required
def consuption_account(account_id):
    """
    Создает транзакцию расхода
    :param account_id: id аккаунта на которм осуществляется транзакция
    """
    form = CreateTransactionsForm()
    account = get_object(Account, account_id)
    response = {
        "title": f"Consuption Account: {account.name}",
        "consuption": True,
        "account_balance": account.balance
    }
    if request.method == "POST":
        if form.validate_on_submit():
            result = account.balance - form.data.get("amount")
            if result >= 0:
                form_data = form_field_pop(form, "csrf_token")
                form_data = adding_required_fields_to_form(
                    form_data, transaction_type="consuption", user_id=current_user.id, account_id=account_id
                )
                account.balance = result
                create_transaction_and_update_account(Transaction, form_data, account)
                flash(message="transaction was successful", category="success")
                return redirect(url_for("index"))

            flash(message="not enough funds", category="info")
            return redirect(url_for("account_router.get_list_accounts"))

        get_errors_field(form)

    return render_template("transaction/transaction_template.html", response=response, form=form)


@transactions_route.route("/transactions-income/<int:account_id>", methods=["GET", "POST"])
@login_required
def income_account(account_id):
    """
    Создает транзакцию для увеличения баланса
    :param account_id: id аккаунта на которм осуществляется транзакция
    """

    form = CreateTransactionsForm()
    account = get_object(Account, account_id)
    response = {
        "title": f"Income Account: {account.name}",
        "income": True,
        "account_balance": account.balance
    }
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = form_field_pop(form, "csrf_token")
            account.balance += form.data.get("amount")
            form_data = adding_required_fields_to_form(
                form_data, transaction_type="income", user_id=current_user.id, account_id=account_id
            )
            create_transaction_and_update_account(Transaction, form_data, account)
            flash(message="transaction was successful", category="success")
            return redirect(url_for("index"))
        get_errors_field(form)
    return render_template("transaction/transaction_template.html", response=response, form=form)


@transactions_route.route("/transactions-list/<int:account_id>")
@login_required
def get_account_transactions_list(account_id):
    """
    Получение всех транзакций конкретного аккаунта
    :param account_id: id аккаунта(счета)
    """

    results = get_all_list_transaction_to_account(Transaction, account_id)
    response = {
        "title": f"All transactions list {current_user.username}",
        "transactions_list": True,
    }
    return render_template(
        "transaction/transaction_list.html", response=response, results=results)


@transactions_route.route("/all-transactions-list")
@login_required
def all_list_transactions():
    """
    Получение списка всех транзакций текущего пользователя
    """

    results = get_list_object(Transaction, current_user.id)
    response = {
        "title": f"All transactions list {current_user.username}",
        "transactions_list": True,
    }
    return render_template(
        "transaction/transaction_list.html", response=response, results=results)


@transactions_route.route("/transactions-delete/<id_transaction>")
@login_required
def delete_transaction(id_transaction):
    """
    Удаляет транзакцию
    :param id_transaction: id транзакции
    """

    delete_object(Transaction, id_transaction)
    return redirect(url_for("transactions_route.get_transactions_list", user_id=current_user.id))

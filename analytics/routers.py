from flask import Blueprint, render_template
from flask_login import login_required, current_user
from utils import get_total_balance
from database.models import Account

analytics_routes = Blueprint("analytics_routes", __name__, template_folder="templates", static_folder="static")


@analytics_routes.route("/total-balance", methods=["GET"])
@login_required
def view_total_balance():
    """
    Просмотр общего баланса, а также количество открытых счетов
    """

    total_balance, total_account = get_total_balance(Account, current_user.id)
    response = {
        "title": f"Total Balance {current_user.username}",
        "total_balance": True
    }
    return render_template(
        "analytics/analytics_template.html", response=response,
        total_balance=total_balance, total_account=total_account
    )

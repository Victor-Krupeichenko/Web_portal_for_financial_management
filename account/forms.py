from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Length
from wtforms import StringField, FloatField
from database.connect_database import session_maker
from database.models import Account


class CreateAccountForm(FlaskForm):
    """
    Форма для создания (добовления), обновления счета
    """

    name = StringField(
        "Name", validators=[DataRequired(), Length(min=3)],
        render_kw={"placeholder": "Name"}
    )
    balance = FloatField("Balance", render_kw={"placeholder": "Balance"})

    def validate_name(self, name):
        """
        :param name: название для счета которое пользователь ввел
        """

        with session_maker() as db_session:
            account = db_session.query(Account).filter(Account.name == name.data).first()
            if account:
                raise ValidationError(message="an account with the same name already exists")

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, ValidationError, NumberRange


class CreateTransactionsForm(FlaskForm):
    """
    Форма для создания транзакции
    """

    amount = FloatField(
        "Amount", validators=[
            DataRequired(), NumberRange(min=0.00, message="the number must be positive")
        ],
        render_kw={"placeholder": "amount"}
    )
    description = StringField("Description", render_kw={"placeholder": "Description"})

    def validate_amount(self, amount):
        """
        Дополнительная валидация поля amount
        :param amount: количество которое ввел пользователь
        """

        decimal_row = str(amount.data).split(".")[1]
        if len(decimal_row) > 2:
            raise ValidationError(message="there must be no more than 2 characters after the period")

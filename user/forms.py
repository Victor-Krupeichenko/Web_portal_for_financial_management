from string import punctuation
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError, Length
from database.connect_database import session_maker
from database.models import User
from passlib.hash import pbkdf2_sha256
from flask_login import login_user, current_user
from flask import session


class RegisterUserForm(FlaskForm):
    """
    Форма для регистрации пользователя
    """

    username = StringField(
        "Username", validators=[DataRequired()], render_kw={"placeholder": "Username"}
    )
    email = EmailField(
        "Emil", validators=[Email(message="email not correct"), DataRequired()],
        render_kw={"placeholder": "Email"}
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(
            min=5, message="password must consist of 5 or more characters"
        )],
        render_kw={"placeholder": "Password"}
    )
    confirm_password = PasswordField(
        "Pssword Confirm", validators=[
            DataRequired(), EqualTo("password", message="passwords don't match")
        ],
        render_kw={"placeholder": "Password confirm"}
    )

    def validate_username(self, username):
        """
        Валидация поля username
        :param username: имя которое ввел пользователь
        """

        with session_maker() as db_session:
            user = db_session.query(User).filter(User.username == username.data).first()
            if user:
                raise ValidationError(message="a user with the same name already exists")
        if len(username.data) < 3 or any(x in punctuation for x in username.data):
            raise ValidationError(message="Invalid username")

    def validate_password(self, password):
        """
        Валидаци поля password
        :param password: пароль который ввел пользователь
        """

        if password.data.isalpha() or password.data.isdigit():
            raise ValidationError(message="password must consist of letters and numbers")

    def validate_email(self, email):
        """
        Валидация поля email
        :param email:  который ввел пользователь
        """

        with session_maker() as db_session:
            user = db_session.query(User).filter(User.email == email.data).first()
            if user:
                raise ValidationError(message="a user with this email already exists")


class UserLogin(FlaskForm):
    """
    Форма для авторизации пользователя
    """

    username = StringField(
        "Username", validators=[
            DataRequired(),
            Length(min=3, message="Invalid username")
        ],
        render_kw={"placeholder": "username"}
    )
    password = PasswordField(
        "Password", validators=[
            DataRequired(), Length(min=5, message="password must consist of 5 or more characters")
        ],
        render_kw={"placeholder": "password"}
    )

    def validate_username(self, username):
        """
        Валидация поля username и поля password
        :param username: имя пользователя которое ввел пользователь
        """
        password = self.password.data
        with session_maker() as db_session:
            user = db_session.query(User).filter(User.username == username.data).first()
            if not user:
                raise ValidationError(message="user with this name does not exist")
            if not pbkdf2_sha256.verify(password, user.password):
                raise ValidationError(message="wrong password")
        # сразу авторизовываем пользователя
        # устанавливаем сеанс с постоянным временем жизни
        # (даже если закроем бравзер пользователь останется авторизованным)
        login_user(user)
        session.permanent = True


class PasswordChangeForm(FlaskForm):
    """
    Форма для изменения пароля
    """

    old_password = PasswordField(
        "OldPassword", validators=[DataRequired()], render_kw={"placeholder": "old password"}
    )
    new_password = PasswordField(
        "NewPassword", validators=[
            DataRequired(), Length(min=5, message="password must consist of 5 or more characters"),
        ],
        render_kw={"placeholder": "new_password"}
    )
    confirm_new_password = PasswordField(
        "ConfirmNewPassword", validators=[
            DataRequired(), EqualTo("new_password", message="passwords don't match")
        ],
        render_kw={"placeholder": "confirm_new_password"}
    )

    def validate_old_password(self, old_password):
        """
        Валидация поля для старого пароля
        :param old_password: старый пароль который ввел пользователь
        """

        if not pbkdf2_sha256.verify(old_password.data, current_user.password):
            raise ValidationError(message="the old password was entered incorrectly")

    def validate_new_password(self, new_password):
        """
        Валидация нового пароля
        :param new_password: Новый пароль который ввел пользователь
        """
        if new_password.data.isalpha() or new_password.data.isdigit():
            raise ValidationError(message="password must consist of letters and numbers")

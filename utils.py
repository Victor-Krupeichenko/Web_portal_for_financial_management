from database.connect_database import session_maker
from flask import flash


def error_database(ex):
    """
    Сообщение об ошибке подключения к базе данных
    :param ex: ошибка которую нужно показать
    """

    flash(message=f"Error: Connect Database -> {ex}", category="danger")


def form_field_pop(form, *fields):
    """
    Удаляет из формы поля которые не нужны для дальнейшей работы с формай
    :param form: данные из html-формы
    :param fields: кортеж полей которые необходимо удалить из формы
    :return: возвращет форму только с необходимыми для дальнейшей работы полями
    """
    form_data = form.data
    for field in fields:
        form_data.pop(field, None)
    return form_data


def create_record_database(model, form_data):
    """
    Создает новую запись в базе данных
    :param model: модель таблицы базы данных в которой нужно создать запись
    :param form_data: данные которые нужно внести в базу данных
    :return: объект модели либо сообщение с ошибкай
    """

    with session_maker() as db_session:
        try:
            new_record = model(**form_data)
            db_session.add(new_record)
            db_session.commit()
            return new_record
        except Exception as ex:
            error_database(ex)


def get_errors_field(form, cat="danger"):
    """
    Получает поля в которых были ошибки
    :param form: все поля формы в которых были ошибки заполнения
    :param cat: категория ошибки
    """

    for field, errors in form.errors.items():
        flash(message=f"Error: {errors.pop(0)}", category=cat)


def get_list_object(model, current_user_id):
    """
    Получение списка объектов из баззы данных
    :param model: модель из которой необходимо получить список объектов
    :param current_user_id: id текущего пользователя для которого необходимо получить список объектов
    :return:  Либо список объектов, либо сообщение с ошибкой
    """

    with session_maker() as db_session:
        try:
            results = db_session.query(model).filter(model.user_id == current_user_id)
            return results
        except Exception as ex:
            error_database(ex)


def get_object(model, object_id):
    """
    Получение объекта модели
    :param model: Модель объект которой необходимо получть
    :param object_id: id необходимого объекта
    :return: Объект модели
    """

    with session_maker() as db_session:
        try:
            result = db_session.query(model).filter(model.id == object_id).first()
            return result
        except Exception as ex:
            error_database(ex)


def apply_changes(obj):
    """
    Обнавляет объект
    :param obj: объект который необъодимо обновить
    """

    with session_maker() as db_session:
        try:
            db_session.add(obj)
            db_session.commit()
        except Exception as ex:
            error_database(ex)


def delete_object(model, object_id):
    """
    Удаление объекта
    :param model: Модель объект которой нужно удалить
    :param object_id: id объекта который нужно удалить
    """

    with session_maker() as db_session:
        try:
            result = db_session.get(model, object_id)
            db_session.delete(result)
            db_session.commit()
            flash(message="entry deleted", category="info")
        except Exception as ex:
            error_database(ex)

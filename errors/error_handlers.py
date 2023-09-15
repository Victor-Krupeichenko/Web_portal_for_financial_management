from flask import render_template


def page_not_found(error):
    """
    Если запрашиваемая страница отсуствует
    :param error: объект ошибки
    :return: возвращает страницу для этой ошибки
    """

    response = {
        "title": "Page Not Found"
    }
    return render_template("errors/error_page.html", response=response), 404


def interval_error_server(error):
    """
    Внутренняя ошибка сервера
    :param error: объект ошибки
    :return: возвращает страницу для этой ошибки
    """

    response = {
        "title": "Interval Error Server"
    }
    return render_template("errors/error_page.html", response=response), 500


def handle_exception(error):
    """
    Обрабатывает исключение которые могут возникнуть
    :param error: объект ошибки
    :return: возвращает страницу для этой ошибки
    """

    response = {
        "title": "Exception"
    }
    return render_template("errors/error_page.html", error=error, response=response), 500

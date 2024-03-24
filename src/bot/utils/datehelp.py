import datetime as dt
from typing import Optional


def datetime_by_format(datetime: str) -> Optional[dt.datetime]:
    """
    Конвертация отформатированной строки в дату.

    :param datetime: Дата в виде строки, день-месяц-год часы-минуты.
    :return: Объект даты.
    """
    datetime = (
        datetime.replace("-", " ").replace(".", " ").replace(",", " ").replace(":", " ")
    )
    try:
        day, month, year, hour, minute = map(int, datetime.strip().split())

        if year < 1000:  # Если не ГГГГ, а ГГ
            year += dt.datetime.utcnow().year // 1000 * 1000

        date_obj = dt.datetime(
            day=day,
            month=month,
            year=year,
            hour=hour,
            minute=minute,
        )
    except ValueError:
        return None

    return date_obj


def weekday_by_date(date: dt.date) -> str:
    """
    День недели по дате.

    :param date: Объект даты.
    :return: День недели в виде строки.
    """
    return (
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье",
    )[date.weekday()]

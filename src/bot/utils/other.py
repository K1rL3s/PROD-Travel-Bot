from aiogram.types import User


def extract_username(from_user: User) -> str | None:
    """
    Получение имени из сообщения или нажатия кнопки.

    :param from_user: От кого событие.
    :return: Имя для бд.
    """
    return from_user.username or from_user.first_name or from_user.last_name

from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ButtonType, InlineKeyboardBuilder

from bot.callbacks import Paginator

PAGE_BACK = "⬅️Назад"
PAGE_FORWARD = "➡️Вперёд"


def paginate_keyboard(
    buttons: list[ButtonType],
    menu: str,
    page: int = 0,
    rows: int = 3,
    width: int = 2,
    additional_buttons: list[InlineKeyboardButton] | None = None,
    fabric: type[Paginator] = Paginator,
    **data: Any,
) -> InlineKeyboardMarkup:
    if data:
        fabric = fabric.init_wrapper(**data)

    builder = InlineKeyboardBuilder()
    bpp = rows * width  # Кнопок на страницу (buttons per page)

    start, end = page * bpp, page * bpp + bpp

    builder.add(*buttons[start:end])
    builder.adjust(width)

    left_right: list[ButtonType] = []
    if page > 0:
        left_right.append(
            InlineKeyboardButton(
                text=PAGE_BACK,
                callback_data=fabric(menu=menu, page=page - 1).pack(),
            )
        )
    if end < len(buttons):
        left_right.append(
            InlineKeyboardButton(
                text=PAGE_FORWARD,
                callback_data=fabric(menu=menu, page=page + 1).pack(),
            )
        )
    builder.row(*left_right, width=2)

    if additional_buttons:
        builder.row(*additional_buttons, width=len(additional_buttons))

    return builder.as_markup()

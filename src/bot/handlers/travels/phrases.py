from aiogram import html

TITLE_ERROR = "❌ Название слишком длинное или ты его использовал, нужно другое."
DESCRIPTION_ERROR = "❌ Описание слишком хорошее, но длинное, его надо сократить."

YOUR_TRAVELS = "🏔️ Вот все путешествия, в которых ты участвуешь"

NOT_ENOUGH_LOCATIONS = "❗ Пока в путешествии мало локаций, чтобы строить маршрут"

ARE_YOU_SURE_DELETE_TRAVEl = """
❓ Вы уверены, что хотите удалить путешествие под названием "{title}"?
❗ Все локации, заметки будут стёрты, а другие участники будут исключены.
""".strip()

ROUTE_URL = """
🌌 Вот маршрут на машине по всем локациям в порядке их посещения.
{url}
""".strip()

PROCESSING = f"""
{html.italic("⚙️⏳ Уточняю данные, секунду...")}
❗Чем больше локаций и чем дальше они друг от друга, тем дольше я буду создавать маршрут
""".strip()
BAD_ROUTE = """
‍😵‍💫❌ Не удалось построить маршрут.
Скорее всего, что-то не так с локациями
""".strip()


error_text_by_field = {
    "title": TITLE_ERROR,
    "description": DESCRIPTION_ERROR,
}

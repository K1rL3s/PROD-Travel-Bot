from core.utils.enums import LocationField

FILL_TITLE = """
1️⃣ Как называется это место?
По названию я помогу тебе определить адрес локации, поэтому желательно ввести существующее место.
Название будет отображаться при просмотре всех локаций.
""".strip()
TITLE_ERROR = """
❌ Кажется, что название слишком длинное, чтобы быть хорошим.
Укоротите его и продолжим создание локации.
""".strip()

FILL_CITY = """
✅ Название записал.
2️⃣ В каком городе (населённом пункте) находится эта локация?
""".strip()
CITY_ERROR = """
❌ Да, оказывается, я знаю не всё в нашем мира.
Если такое место всё же существует, то попробуй написать его название как оно есть, я обязательно постараюсь его найти.
""".strip()

FILL_COUNTRY = """
✅ Нашёл это место.
3️⃣ Чтобы между нами точно не было недопонимания, выбери, в какой это стране?
Нажми на один из вариантов ниже, только эти страны я могу предположить.
"""
COUNTRY_ERROR = """
❌ Мне кажется, что тут что-то не так.
Если именно эта страна, то моя оценка по географии точно завышена.
Попробуй ввести страну ещё раз или выбери любую, после создания лоакции ты сможешь изменить её.
""".strip()

FILL_ADDRESS = """
✅ Страну запомнил.
4️⃣ Знаешь адрес? Если я его знаю, то снизу отправил тебе подсказку.
""".strip()
ADDRESS_ERROR = "❌ Адрес слишком большой. Пожалуйста, сократи его и отправь снова."

FILL_START_AT = """
✅ Адрес сохранил.
5️⃣ Остался последний шаг. Введите дату и время, в которое вы хотите там быть.
По этому времени я определю порядок локаций и буду строить маршрут.
Формат - "ДД.ММ.ГГГГ ЧЧ:ММ" или "День Месяц Год Часы Минуты" через пробел.
""".strip()
START_AT_ERROR = """
❌ Кажется, что мы с вами не сошлись в форматах.
Попробуйте ввести время как "ДД ММ ГГГГ ЧЧ ММ".
""".strip()

error_text_by_field = {
    LocationField.TITLE: TITLE_ERROR,
    LocationField.COUNTRY: COUNTRY_ERROR,
    LocationField.CITY: CITY_ERROR,
    LocationField.ADDRESS: ADDRESS_ERROR,
    LocationField.START_AT: START_AT_ERROR,
}

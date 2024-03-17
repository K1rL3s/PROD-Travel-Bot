from bot.utils.enums import ProfileFields

NAME_TOO_LONG = "Имя слишком длинное. Введите его короткую версию."
AGE_INVALID = "Возраст должен быть настоящим и числом. Введите его ещё раз."
CITY_TOO_LONG = (
    "Название города слишком большое, я таких городов не знаю. "
    "Введите его короткую версию."
)
DESCRIPTION_TOO_LONG = "Слишком много о себе вы пишите. Давайте ещё раз, но короче"

error_text_by_field = {
    ProfileFields.NAME: NAME_TOO_LONG,
    ProfileFields.AGE: AGE_INVALID,
    ProfileFields.CITY: CITY_TOO_LONG,
    ProfileFields.DESCRIPTION: DESCRIPTION_TOO_LONG,
}

from core.utils.enums import ProfileField

NAME_ERROR = "Имя слишком длинное. Введите его короткую версию."
AGE_ERROR = "Возраст должен быть настоящим и числом. Введите его ещё раз."
CITY_ERROR = (
    "Название города слишком большое, я таких городов не знаю. "
    "Введите его короткую версию."
)
DESCRIPTION_ERROR = "Слишком много о себе вы пишите. Давайте ещё раз, но короче"

error_text_by_field = {
    ProfileField.NAME: NAME_ERROR,
    ProfileField.AGE: AGE_ERROR,
    ProfileField.CITY: CITY_ERROR,
    ProfileField.DESCRIPTION: DESCRIPTION_ERROR,
}

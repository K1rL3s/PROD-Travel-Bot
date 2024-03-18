from core.utils.enums import LocationField

TITLE_ERROR = "Ошибка в названии"
COUNTRY_ERROR = "Ошибка в стране"
CITY_ERROR = "Ошибка в городе"
ADDRESS_ERROR = "Ошибка в месте"
START_AT_ERROR = "Ошибка в времени начала"
END_AT_ERROR = "Ошибка в времени конца"

error_text_by_field = {
    LocationField.TITLE: TITLE_ERROR,
    LocationField.COUNTRY: COUNTRY_ERROR,
    LocationField.CITY: CITY_ERROR,
    LocationField.ADDRESS: ADDRESS_ERROR,
    LocationField.START_AT: START_AT_ERROR,
    LocationField.END_AT: END_AT_ERROR,
}

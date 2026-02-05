from enum import StrEnum


class Texts(StrEnum):
    settings_null = "[не выбрано]"

    settings = "⚙️ Настройки"

    period_up = "Период роста"
    period_down = "Период просадки"
    percent_up = "Процент роста"
    percent_down = "Процент просадки"


PERIODS = {
    "1": 1,
    "5": 5,
    "15": 15,
    "30": 30,
    "45": 45,
    "1ч": 60,
    "4ч": 240,
    "24ч": 1440,
}

CBK_DATA_PERIOD_UP = "period_up:"

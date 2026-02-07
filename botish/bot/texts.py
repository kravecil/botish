from enum import StrEnum


class ButtonCaption(StrEnum):
    settings = "⚙️ Настройки"  # TODO @me: переместить отсюда

    period_up = "Период роста"
    period_down = "Период просадки"
    percent_up = "Процент роста"
    percent_down = "Процент просадки"

    back_to_settings = "⬅️ Назад"


TXT_SETTINGS_NULL = "[не выбрано]"

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

CLBK_SETTINGS_CHANGED = "settings_changed"


class SettingsCallback(StrEnum):
    period_up = "period_up"
    period_down = "period_down"
    percent_up = "percent_up"
    percent_down = "percent_down"

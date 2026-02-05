from datetime import datetime


def from_timestamp_ms(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp / 1000)

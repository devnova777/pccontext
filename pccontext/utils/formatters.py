from datetime import datetime

__all__ = ["format_date", "DATE_FORMAT_1", "DATE_FORMAT_2"]

# Fri Jul 22 14:39:46 EST 2022
DATE_FORMAT_1 = "%a %b %d %H:%M:%S %Z %Y"

# Mon, 25 Jul 2022 21:43:09 -0400
DATE_FORMAT_2 = "%a, %d %b %Y %H:%M:%S %z"


def format_date(date: datetime, format: str = DATE_FORMAT_2) -> str:
    """
    Format the date to a string
    :param format:
    :param date: The date
    :return: The formatted date
    """
    if isinstance(date, str):
        return date
    return date.astimezone().strftime(format)

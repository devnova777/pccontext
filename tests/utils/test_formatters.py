import pytest
from datetime import datetime
from pccontext.utils.formatters import format_date

DATE_FORMAT_2 = "%Y-%m-%d %H:%M:%S"


@pytest.mark.parametrize(
    "date, format, expected",
    [
        # Happy path tests
        (datetime(2023, 10, 1, 12, 0, 0), DATE_FORMAT_2, "2023-10-01 12:00:00"),
        (datetime(2023, 1, 1, 0, 0, 0), "%d/%m/%Y", "01/01/2023"),
        (
            datetime(2023, 12, 31, 23, 59, 59),
            "%Y-%m-%d %H:%M:%S",
            "2023-12-31 23:59:59",
        ),
        # Edge cases
        (datetime(1970, 1, 1, 0, 0, 0), DATE_FORMAT_2, "1970-01-01 00:00:00"),
        # Error cases
        (
            "2023-10-01 12:00:00",
            DATE_FORMAT_2,
            "2023-10-01 12:00:00",
        ),  # date is already a string
    ],
    ids=[
        "happy_path_default_format",
        "happy_path_custom_format",
        "happy_path_end_of_year",
        "edge_case_epoch",
        "error_case_string_input",
    ],
)
def test_format_date(date, format, expected):
    # Act
    result = format_date(date, format)

    # Assert
    assert result == expected

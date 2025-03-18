
from datetime import datetime
from freezegun import freeze_time
from utils.time_funcs import last_15_minute_mark

@freeze_time("2024-03-18 14:37:12.345678")
def test_last_15_minute_mark():
    result = last_15_minute_mark()
    assert result == "202403181430" + "00"

@freeze_time("2024-03-18 14:15:00.000000")
def test_last_15_minute_mark_exact():
    result = last_15_minute_mark()
    assert result == "202403181415" + "00"

@freeze_time("2024-03-18 14:00:00.000000")
def test_last_15_minute_mark_hour_boundary():
    result = last_15_minute_mark()
    assert result == "202403181400" + "00"

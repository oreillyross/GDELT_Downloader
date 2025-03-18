from datetime import datetime, timedelta


def last_15_minute_mark():
  now = datetime.now()
  # Calculate the minutes to subtract to get to the last 15-minute mark
  minutes_to_subtract = now.minute % 15
  # Subtract the minutes and reset seconds and microseconds to zero
  closest_time = now - timedelta(minutes=minutes_to_subtract,
                                 seconds=now.second,
                                 microseconds=now.microsecond)
  return closest_time.strftime('%Y%m%d%H%M') + '00'
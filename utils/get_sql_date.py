from datetime import datetime


def get_sqldate_today():
  return int(datetime.today().strftime('%Y%m%d'))  
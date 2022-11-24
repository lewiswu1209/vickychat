
from datetime import datetime

def get_interval_minutes_by_timestamp(timestamp_1, timestamp_2):
    if timestamp_1 > timestamp_2:
        timestamp_1, timestamp_2 = timestamp_2, timestamp_1
    timestamp_1 = int(timestamp_1)
    timestamp_2 = int(timestamp_2)
    minutes = (timestamp_2 - timestamp_1) / 60
    return minutes

def get_interval_years_by_date_str(date1, date2):
    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    if date1.timestamp() > date2.timestamp():
        date1, date2 = date2, date1
    return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))

def get_year_by_date_str(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.year

def get_month_by_date_str(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.month

def get_day_by_date_str(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.day

def get_current_datetime():
    return datetime.now()

def get_current_datetime_str():
    return datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')

def get_datetime_str_by_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y年%m月%d日 %H:%M:%S')

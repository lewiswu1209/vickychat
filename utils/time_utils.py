
from datetime import datetime

def get_year_diff(date1, date2):
    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))

def get_year_by_date(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.year

def get_month_by_date(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.month

def get_day_by_date(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.day

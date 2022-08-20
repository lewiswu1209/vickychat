
from datetime import datetime

def get_year_diff(date1, date2):
    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))

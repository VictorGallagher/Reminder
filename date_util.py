# date_util.py


from wx import DateTime
from datetime import datetime
#from dateutil.relativedelta import *
from dateutil import relativedelta
'''useful date functions'''

def add_minutes(d, n):
    return d + relativedelta(minutes=+n)


def add_hours(d, n):
    return d + relativedelta(hours=+n)


def add_days(d, n):
    return d + relativedelta(days=+n)


def add_weeks(d, n):
    return d + relativedelta(weeks=+n)


def add_months(d, n):
    return d + relativedelta(months=+n)


def add_years(d, n):
    return d + relativedelta(years=+n)


def get_weekday_name(self, d):
    days = ['Sunday', 'Monday', 'Tuesday',
            'Wenesday', 'Thursday', 'Friday', 'Saturday']
    return days[d]


def get_month_name(self, m):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    return months[m]


def get_sufix(self, d):
    if d == 2:
        return '\'nd'
    elif d == 3:
        return '\'rd'
    else:
        return '\'th'


def convert_wxDateTime_to_datetime(mwxDateTime):
    # Converts a value wx.DateTime into a datetime.datetime
    return datetime(
        int(mwxDateTime.GetYear()), 
        int(mwxDateTime.GetMonth() + 1),
        int(mwxDateTime.GetDay()),
        int(mwxDateTime.GetHour()),
        int(mwxDateTime.GetMinute())
    )


def convert_datetime_to_wxDateTime(pyDateTime):
    return DateTime(
        int(pyDateTime.year),
        int(pyDateTime.month) - 1,
        int(pyDateTime.day),
        int(pyDateTime.hour),
        int(pyDateTime.minute))


def splice_wxDate_wxTime(date, time):
    '''Merge a date with a time, takes wxDate and wxTime'''
    date.hour = time.hour
    date.minute = time.minute
    date = convert_wxDateTime_to_datetime(date)
    return date


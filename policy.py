#policy.py

'''Policy and Reminder classes'''
import uuid
import wx
from datetime import datetime
import date_util as du


class Policy(object):
    def __init__(self, title='Title', message='message',
                 s_time=None, date=wx.DateTime.Today(), period='Daily',
                 message_type='Notification', t_time=wx.DateTime.Today()):
        self.id = uuid.uuid1()
        self.title = title
        self.message = message
        self.s_time = s_time
        self.t_time = t_time
        self.date = date
        self.period = period
        self.message_type = message_type
        self.prd = {'Daily': 7, 'Weekly': 4, 'Monthly': 3,
                    'Anually': 2, 'One Time Only': 1}

    def get_nth_policy_date(self, n=1):
        if self.period == 'Daily':
            return du.add_days(self.date, n)
        elif self.period == 'Weekly':
            return du.add_weeks(self.date, n)
        elif self.period == 'Monthly':
            return du.add_months(self.date, n)
        elif self.period == 'Anually':
            return du.add_years(self.date, n)
        else:
            pass

    def update_policy_date(self):
        print(self)
        while self.date < datetime.now():
            self.date = self.get_nth_policy_date(1)

    def get_last_policy_date(self):
        return self.get_nth_policy_date(self.prd[self.period])

    def advance_policy_time(self, n=30):
        self.date = du.add_minutes(self.date, n)

#    def __str__(self):
#        return str(self.__class__) + ': ' + str(self.__dict__)

    def __repr__(self):
        ret_str = ''
        d = self.__dict__
        for key in d:
            if not key == 'prd':
                ret_str += ''.join('    <' + str(key) + '>' +
                                   str(d[key]) + '</' + str(key) + '>\n')
        ret_str = '<policy>\n' + ret_str + '</policy>\n'
        return ret_str

    def __str__(self):
        ret_str = ''
        d = self.__dict__
        for key in d:
            if not key == 'prd':
                ret_str += ''.join('    <' + str(key) + '>' +
                                   str(d[key]) + '</' + str(key) + '>\n')
        ret_str = '<policy>\n' + ret_str + '</policy>\n'
        return ret_str


class Reminder(object):
    def __init__(self, title, message, s_time, exec_datetime, period, message_type, id, timer):
        self.title = title
        self.message = message
        self.s_time = s_time
        self.exec_datetime = exec_datetime
        self.period = period
        self.message_type = message_type
        self.id = id
        self.timer = timer

    def advance_reminder_time(self, n=30):
        self.exec_datetime = du.add_minutes(self.date, n)

    def cancel_timer(self):
        self.timer.cancel()

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)

    def __repr__(self):
        ret_str = ''
        d = self.__dict__
        for key in d:
            if not key == 'prd':
                ret_str += ''.join('    <' + str(key) + '>' +
                                   str(d[key]) + '</' + str(key) + '>\n')
        ret_str = '<reminder>\n' + ret_str + '</reminder>\n'
        return ret_str



def create_policly_sentence(plcy):
    '''Convert policy attributes into a legible sentence  '''
    if plcy.period == 'Daily':
        sentence = 'Execute \'' + \
            str(plcy.title) + '\' every day at ' + str(plcy.s_time) + '.'
        return sentence
    elif plcy.period == 'Weekly':
        weekday = du.get_weekday_name(plcy.date.weekday())
        sentence = 'Execute \'' + \
            str(plcy.title) + '\' every ' + str(weekday) + \
            ' at ' + str(plcy.s_time) + '.'
        return sentence
    elif plcy.period == 'Monthly':
        day = plcy.date.day
        sentence = 'Execute \'' + str(plcy.title) + '\' on the ' + str(
            day) + du.get_sufix(day) + ' of every month at ' + str(plcy.s_time) + '.'
        return sentence
    elif plcy.period == 'Anually':
        day = plcy.date.day
        month = du.get_month_name(plcy.date.month)
        sentence = 'Execute \'' + plcy.title + '\' on the ' + \
            str(day) + du.get_sufix(day) + ' of every ' + \
            month + ' at ' + str(plcy.s_time) + '.'
        return sentence
    else:
        sentence = 'Execute \'' + str(plcy.title) + '\' on ' + str(
            plcy.date.strftime('%A %B %d %Y')) + ' at ' + str(plcy.s_time) + '.'
        return sentence
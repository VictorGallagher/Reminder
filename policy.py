#policy.py

'''Policy and Reminder classes'''
import uuid
import wx
from datetime import datetime
import date_util as du


class Policy(object):
    ''' t_time needs to be removed also dates should be stored and datetime not wxDateTime'''
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
        ''' Find a future date for the policy. Intentionaly left 
        incomplete for futher exention'''
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
        ''' Increment policy date until date is in the future.'''
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
        self.s_time = s_time #time of day as a string
        self.exec_datetime = exec_datetime #the execution time and date for the reminder
        self.period = period
        self.message_type = message_type
        self.id = id # id of the policy the reminder was derived from
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


def create_reminder_instance(plcy, dt):
    '''timer is set in the MainFrame object'''
    rmdr = Reminder(plcy.title, plcy.message, plcy.s_time,
                    dt, plcy.period, plcy.message_type, plcy.id, timer=0)
    return rmdr

def create_new_reminder(plcy, i):
    '''Takes a policy object and a period increment.
    Returns a reminder instance for the given policy and increment.'''
    if plcy.period == 'Daily':
        dt = du.add_days(plcy.date, i)
        if not dt < datetime.now():
            rmdr = create_reminder_instance(plcy, dt)
            return rmdr
    elif plcy.period == 'Weekly':
        dt = du.add_weeks(plcy.date, i)
        if not dt < datetime.now():
            rmdr = create_reminder_instance(plcy, dt)
            return rmdr
    elif plcy.period == 'Monthly':
        dt = du.add_months(plcy.date, i)
        if not dt < datetime.now():
            rmdr = create_reminder_instance(plcy, dt)
            return rmdr
    elif plcy.period == 'Anually':
        dt = du.add_years(plcy.date, i)
        if not dt < datetime.now():
            rmdr = create_reminder_instance(plcy, dt)
            return rmdr
    else:
        dt = plcy.date
        if not dt < datetime.now():
            rmdr = create_reminder_instance(plcy, dt)
            return rmdr

def create_pending_reminders(plcy):
    '''Takes a policy instance an generates its pending
    reminder instances, depending on the 'per' dictionary'''
    per = {'Daily': 7, 'Weekly': 4, 'Monthly': 3,
           'Anually': 2, 'One Time Only': 1}
    p = per[plcy.period]
    reminder_list = []
    for i in range(0, p):
        rmdr = create_new_reminder(plcy, i)
        if rmdr is not None:
            reminder_list.append(rmdr)
    return reminder_list


def build_reminder_list(plcyl):
    '''Steps through all the policies and builds a
    list of reminder instances from them.'''
    rml = [] #reminder list
    for plcy in plcyl:
        rml.extend(create_pending_reminders(plcy))
    rml = sorted(rml, key=lambda rmdr: rmdr.exec_datetime)
    return rml




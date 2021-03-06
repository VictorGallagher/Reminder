

# -*- encoding: utf-8
#from tendo import singleton
import wx
import wx.adv
import wx.lib.masked as masked
import wx.html
from wx.lib.wordwrap import wordwrap

from datetime import *
import sys
import date_util as du
import policy as pl
import copy



class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(-1, -1)):
        wx.html.HtmlWindow.__init__(self, parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()


class helpDlg(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, wx.ID_ANY,
                          title="About", size=(400, 400))
        html = HtmlWindow(self, -1, size=(400, 400))
        html.SetPage(
            ''
            "<h2>Reminder Rules</h2>"
            "<p>This aplication allows the user to easily create repeating reminders, presented as "
            "a notification or a question. To create a reminder of either type, first create a 'policy'. "
            "A policy is a set of general rules the aplication uses for creating reminders. "
            "Once the aplication has a policy to work with it creates a list of pending reminders, "
            "sorted in ascending order by date. To edit a policy simply double click it in the policy list.</p>"
            "<p><b>by Victor Gallagher</h3></p>"
        )


class PolicyDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title='Create a Reminder')
        periods = ['One Time Only', 'Daily', 'Weekly', 'Monthly', 'Anually']
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.calen_ctrl = wx.adv.GenericCalendarCtrl(self, -1,
                                                     wx.DateTime.Today(), size=(300, 200), pos=(5, 5),
                                                     style=wx.adv.CAL_SHOW_HOLIDAYS)
        self.calen_ctrl.Enable(False)
        self.stext4 = wx.StaticText(self, -1, '  Title:')
        self.title_box = wx.TextCtrl(self, -1, '', size=(-1, -1))
        self.stext5 = wx.StaticText(self, -1, '  Contents:')
        self.message_box = wx.TextCtrl(
            self, -1, '', size=(-1, -1), style=wx.TE_MULTILINE)
        self.message_box.Enable(False)
        self.stext3 = wx.StaticText(self, -1, '  Set Date and Time of Day')
        self.time_ctrl = masked.TimeCtrl(
            self, -1, name='time of day', display_seconds=False)
        self.time_ctrl.Enable(False)
        self.stext1 = wx.StaticText(self, -1, '  Reacuring Period:')
        self.periods_combo = wx.ComboBox(
            self, choices=periods, style=wx.CB_READONLY | wx.CB_DROPDOWN)
        # self.periods_combo.SetValue('Daily')
        self.periods_combo.Enable(False)
        self.stext2 = wx.StaticText(self, -1, '  Reminder Type:')
        self.message_type_combo = wx.ComboBox(
            self, choices=['Notification', 'Question'], style=wx.CB_READONLY | wx.CB_DROPDOWN)
        # self.message_type_combo.SetValue('Notification')
        self.message_type_combo.Enable(False)
        self.reminder_verify = wx.TextCtrl(self, -1, '', size=(-1, -1),
                                           style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.ok_button = wx.Button(self, id=wx.ID_OK, label='Ok')
        self.ok_button.Enable(False)
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnDialogButton)
        cancel_button = wx.Button(self, id=wx.ID_CANCEL, label='Cancel')
        cancel_button.Bind(wx.EVT_BUTTON, self.OnDialogButton)
        sizer.Add(self.stext4, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.title_box, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.stext5, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.message_box, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.stext3, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.time_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.calen_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.stext1, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.periods_combo, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.stext2, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.message_type_combo, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.reminder_verify, 0, wx.ALL | wx.EXPAND, 5)
        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        bsizer.AddSpacer(50)
        bsizer.Add(self.ok_button, 0, wx.ALL, 5)
        bsizer.Add(cancel_button, 0, wx.ALL, 5)
        sizer.Add(bsizer, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Fit(self)
        self.SetSizer(sizer)
        self.CenterOnScreen()
        self.Show()
        self.title_box.Bind(wx.EVT_TEXT, self.on_event_title_box)
        self.message_box.Bind(wx.EVT_TEXT, self.on_event_message_box)
        self.time_ctrl.Bind(wx.EVT_TEXT, self.on_event_time_ctrl)
        self.calen_ctrl.Bind(wx.adv.EVT_CALENDAR, self.on_event_calen_ctrl)
        self.periods_combo.Bind(wx.EVT_TEXT, self.on_event_periods_combo)
        self.message_type_combo.Bind(
            wx.EVT_TEXT, self.on_event_message_type_combo)

    def on_event_title_box(self, event):
        self.message_box.Enable(True)

    def on_event_message_box(self, event):
        self.time_ctrl.Enable(True)

    def on_event_time_ctrl(self, event):
        self.calen_ctrl.Enable(True)

    def on_event_calen_ctrl(self, event):
        self.periods_combo.Enable(True)

    def on_event_periods_combo(self, event):
        self.message_type_combo.Enable(True)

    def on_event_message_type_combo(self, event):
        self.ok_button.Enable(True)
        self.reminder_verify.Clear()
        title = self.title_box.GetValue()
        message = self.message_box.GetValue()
        time = self.time_ctrl.GetValue()
        wxtime = self.time_ctrl.GetValue(as_wxDateTime=True)
        wxdate = self.calen_ctrl.GetDate()
        date = du.splice_wxDate_wxTime(wxdate, wxtime)
        period = self.periods_combo.GetValue()
        message_type = self.message_type_combo.GetValue()
        self.plcy = pl.Policy(title, message, time, date, period, message_type, wxtime)
        if date < datetime.now():
            print('Main File date ', date)
            self.plcy.update_policy_date()
        discription = self.plcy.get_policy_discription()
        self.reminder_verify.SetBackgroundColour('lightblue')
        self.reminder_verify.AppendText(discription) 

    def OnDialogButton(self, event):
        e = event.GetEventObject()
        label = e.GetLabel()

        if label == 'Ok':
            self.EndModal(wx.ID_OK)
            return self.plcy
        elif label == 'Cancel':
            self.EndModal(wx.ID_CANCEL)

class SysTray(wx.adv.TaskBarIcon):  

    def __init__(self, parent, icon, text):
        wx.adv.TaskBarIcon.__init__(self)
        self.parentApp = parent
        self.SetIcon(icon, text)
        self.CreateMenu()

    def CreateMenu(self):
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.ShowMenu)
        self.menu = wx.Menu()
        self.menu.Append(wx.ID_OPEN, "Show")
        self.menu.Append(wx.ID_EXIT, "Close")

    def ShowMenu(self, event):
        self.PopupMenu(self.menu)


class MainFrame(wx.Frame):
    custom_style = (wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                    wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.RESIZE_BORDER)

    def __init__(self, title='Reminder', pos=(10, 10), size=(700, 650), style=wx.SIMPLE_BORDER | custom_style):
        wx.Frame.__init__(self, None, id=-1, title=title, pos=pos, size=size)
        self.name = "ReminderApp-%s" % wx.GetUserId()
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            self.Destroy()
        image = wx.Image('reminder_finger2.png',
                         wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.Icon()
        icon.CopyFromBitmap(image)
        self.SetIcon(icon)
        self.trayicon = SysTray(self, icon, 'Test')
        self.policy_list = []
        self.reminder_list = []
        menuBar = wx.MenuBar()
        policymenu = wx.Menu()
        menuBar.Append(policymenu, '&Policy')
        create_policy_menu_item = policymenu.Append(wx.NewId(), '&Create')
        edit_policy_menu_item = policymenu.Append(wx.NewId(), '&Edit', '')
        delete_policy_menu_item = policymenu.Append(wx.NewId(), '&Delete')
        policymenu.AppendSeparator()
        close_menu_item = policymenu.Append(wx.ID_EXIT, '&Close')
        helpmenu = wx.Menu()
        menuBar.Append(helpmenu, '&Help')
        help_menu_item = helpmenu.Append(wx.NewId(), '&Help')
        about_menu_item = helpmenu.Append(wx.ID_ABOUT, '&About', 'About Reminder')
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onAboutDlg, about_menu_item)
        self.Bind(wx.EVT_MENU, self.onHelpHtmlDlg, help_menu_item)
        self.Bind(wx.EVT_MENU, self.on_create_policy_btn,
                  create_policy_menu_item)
        self.Bind(wx.EVT_MENU, self.on_policy_listbox_doubleclick,
                  edit_policy_menu_item)
        self.Bind(wx.EVT_MENU, self.on_close, close_menu_item)
        self.Bind(wx.EVT_MENU, self.on_delete_btn, delete_policy_menu_item)
        #self.trayicon.Bind(wx.EVT_MENU, self.on_close, wx.ID_EXIT)
        #self.trayicon.Bind(wx.EVT_MENU, self.Show, wx.ID_ANY)
        self.p_panel = wx.Panel(self, wx.ID_ANY)
        ptext1 = wx.StaticText(self.p_panel, -1, '  Policies:')
        self.policy_listbox = wx.ListBox(
            self.p_panel, -1, size=(-1, 150), style=wx.LB_SINGLE)
        ptext2 = wx.StaticText(self.p_panel, -1, '  Pending Reminders:')
        self.reminder_listctrl = wx.ListCtrl(self.p_panel, -1, size=(-1, 300),
                                             style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES)
        self.reminder_listctrl.InsertColumn(0, 'Date  ', width=200)
        self.reminder_listctrl.InsertColumn(1, 'Time  ', width=100)
        self.reminder_listctrl.InsertColumn(2, 'Title ', width=125)
        self.reminder_listctrl.InsertColumn(3, 'Period', width=125)
        self.reminder_listctrl.InsertColumn(4, 'Type  ', width=125)
        cp_button = wx.Button(self.p_panel, -1, label='Create Policy')
        self.Bind(wx.EVT_BUTTON, self.on_create_policy_btn, cp_button)
        delete_button = wx.Button(self.p_panel, label='Delete Policy')
        delete_button.Bind(wx.EVT_BUTTON, self.on_delete_btn)
        close_button = wx.Button(self.p_panel, label='Close')
        close_button.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(ptext1, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.Add(self.policy_listbox, 0, wx.EXPAND |
                  wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.Add(ptext2, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.Add(self.reminder_listctrl, 0, wx.EXPAND |
                  wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.AddSpacer(25)
        b_sizer = wx.BoxSizer(wx.HORIZONTAL)
        b_sizer.Add(cp_button, 0, wx.ALL | wx.CENTER, 5)
        b_sizer.Add(close_button, 0, wx.ALL | wx.CENTER, 5)
        b_sizer.Add(delete_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(b_sizer, 0, wx.ALL | wx.CENTER, 5)
        self.p_panel.SetSizer(sizer)
        self.policy_listbox.Bind(wx.EVT_LEFT_DCLICK, self.on_policy_listbox_doubleclick)
        #self.Bind(wx.EVT_ICONIZE, self.onMinimize)

        from xml.dom import minidom as md
        try:
            xml_file = open('policies.rmdr', 'r')
        except(IOError) as e:
            print ('I/O error({0}): {1}').format(e.errno, e.strerror)
            try:
                print('Trying backup')
                xml_file = open('policies.bkup', 'r')
            except(IOError) as e:
                print ('I/O error({0}): {1}').format(e.errno, e.strerror)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                xml_file.close()
                sys.exit()
        xml_data = md.parse(xml_file)
        policies = xml_data.getElementsByTagName('policy')
        for policy in policies:
            title = policy.getElementsByTagName(
                'title')[0].firstChild.nodeValue
            message = policy.getElementsByTagName(
                'message')[0].firstChild.nodeValue
            s_time = policy.getElementsByTagName(
                's_time')[0].firstChild.nodeValue
            date = policy.getElementsByTagName(
                'date')[0].firstChild.nodeValue
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            #    date = datetime.strptime(date, '%a %b %d %H:%M:%S %Y')
            period = policy.getElementsByTagName(
                'period')[0].firstChild.nodeValue
            message_type = policy.getElementsByTagName(
                'message_type')[0].firstChild.nodeValue
            t_time = policy.getElementsByTagName(
                't_time')[0].firstChild.nodeValue
            if not(date < datetime.now() and period == 'One Time Only'):
                policy = (pl.Policy(title, message, s_time,
                                 date, period, message_type, t_time))
                policy.update_policy_date()
                self.policy_list.append(policy)
        self.save_to_xml()
        self.update_policy_box()
        self.reminder_list = pl.build_reminder_list(self.policy_list)
        self.start_timers_for_all_reminders(self.reminder_list)
        self.show_pending_reminders()

#    def onMinimize(self, event):
#        if self.IsIconized():
#            self.Hide()

    def onHelpHtmlDlg(self, event):
        help_dlg = helpDlg(None)
        help_dlg.Show()

    def on_delete_btn(self, event):
        index = self.policy_listbox.GetSelection()
        p = self.policy_list[index]
        self.delete_policy(p)
        self.save_to_xml()
        self.update_policy_box()
        self.show_pending_reminders()

    def delete_policy(self, plcy):
        for rmdr in self.reminder_list:
            if rmdr.id == plcy.id:
                self.reminder_list.remove(rmdr)
        for p in self.policy_list:
            if p is plcy:
                self.policy_list.remove(p)

    def create_timer(self, plcy, dt):
        delay = (dt - datetime.now())
        #t = threading.Timer(delay.total_seconds(), self.dispatch_dialog, [delay, dt, plcy])
        #t.setDaemon(True)
        t = wx.CallLater(delay.total_seconds()*1000, self.dispatch_dialog, delay=delay, dt=dt, plcy=plcy)
        return t

    def start_reminder_timers_for_this_policy(self, plcy):
        for rmdr in self.reminder_list:
            if rmdr.id == plcy.id:
                rmdr.timer = self.create_timer(plcy, rmdr.exec_datetime)
                #rmdr.timer.start()
                rmdr.timer.Start()

    def start_timers_for_all_reminders(self, rmdrl):
        for plcy in self.policy_list:
            self.start_reminder_timers_for_this_policy(plcy)

    def delete_policy_reminders(self, plcy):
        for rmdr in self.reminder_list:
            if rmdr.id == plcy.id:
                self.reminder_list.remove(rmdr)

    def save_to_xml(self):
        bkup = open('policies.bkup', 'w')
        file = open('policies.rmdr', 'w')
        file.write('<policies>\n')
        bkup.write('<policies>\n')
        for p in self.policy_list:
            file.write(str(p))
            bkup.write(str(p))
        file.write('</policies>')
        bkup.write('</policies>')
        file.close()
        bkup.close()

    def cancel_all_timers(self):
        for rmdr in self.reminder_list:
            rmdr.timer.Stop()
            del rmdr

    def add_pending_reminder(self, rmdr):
        index = self.reminder_listctrl.InsertItem(
            sys.maxsize, str(rmdr.exec_datetime.strftime('%A, %b-%d, %Y')))
        self.reminder_listctrl.SetItem(index, 1, rmdr.s_time)
        self.reminder_listctrl.SetItem(index, 2, rmdr.title)
        self.reminder_listctrl.SetItem(index, 3, rmdr.period)
        self.reminder_listctrl.SetItem(index, 4, rmdr.message_type)
        return index

    def dispatch_dialog(self, delay, dt, plcy):
        # decides wich dialog to use
        if plcy.message_type == 'Notification':
            wx.CallAfter(self.reminder_dlg, plcy.message, plcy.title)
            self.reminder_list.pop(0)
            if not plcy.period == 'One Time Only':
                plcy.update_policy_date()
                dt = plcy.get_last_policy_date()
                self.reminder_list.append(
                    pl.create_reminder_instance(plcy, dt))
            else:
                self.delete_policy(plcy)
                self.update_policy_box()
            self.show_pending_reminders()
        else: # handle question dialog results
            wx.CallAfter(self.question_dlg, plcy)
            if not plcy.period == 'One Time Only':
                plcy.update_policy_date()
                dt = plcy.get_last_policy_date()
                self.reminder_list.append(
                    pl.create_reminder_instance(plcy, dt))
            else:
                self.reminder_list.pop(0)
                self.delete_policy(plcy)
                self.update_policy_box()
            self.show_pending_reminders()

    def show_pending_reminders(self):
        self.reminder_listctrl.DeleteAllItems()
        self.reminder_list = sorted(
            self.reminder_list, key=lambda rmdr: rmdr.exec_datetime)
        for rmdr in self.reminder_list:
            index = self.add_pending_reminder(rmdr)
            if index % 2:
                self.reminder_listctrl.SetItemBackgroundColour(index, 'white')
            else:
                self.reminder_listctrl.SetItemBackgroundColour(index, 'lightblue')

    def reminder_dlg(self, msg, cptn):
        dlg = wx.MessageDialog(
            None, message=msg, caption=cptn, style=wx.OK | 
                wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        result = dlg.ShowModal()
        if result == wx.OK:
            dlg.Destroy()
        else:
            dlg.Destroy()

    def question_dlg(self, plcy):
        dlg = wx.MessageDialog(self, message=plcy.message, caption=plcy.title,
                style=wx.YES_NO | wx.ICON_QUESTION | wx.YES_DEFAULT | wx.STAY_ON_TOP)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()
        else:
            if plcy.period == 'One Time Only':
                plcy.advance_policy_minutes(30)
                new_time = copy.copy(plcy.date)
                new_policy = copy.copy(plcy)
                new_policy.s_time = new_time.strftime('%I:%M %p')
                self.policy_list.append(new_policy)
                rmdr = new_policy.create_reminder_instance(new_time)
                rmdr.s_time = new_policy.s_time
                self.reminder_list.append(rmdr)
                self.reminder_list = sorted(self.reminder_list,
                            key=lambda rmdr: rmdr.exec_datetime)
                self.start_reminder_timers_for_this_policy(new_policy)
                self.update_policy_box()
                self.show_pending_reminders()
            else:
                new_time = datetime.now()
                new_time = du.add_minutes(new_time, 30)
                rmdr = plcy.create_reminder_instance(new_time)
                rmdr.s_time = new_time.strftime('%I:%M %p')
                rmdr.timer = self.create_timer(plcy, new_time)
                self.reminder_list.append(rmdr)
                self.reminder_list.pop(0)
                self.reminder_list = sorted(self.reminder_list,
                            key=lambda rmdr: rmdr.exec_datetime)
                self.update_policy_box()
                self.show_pending_reminders()
            dlg.Destroy()

    def update_policy_box(self):
        self.policy_list = sorted(
            self.policy_list, key=lambda plcy: plcy.date)
        self.policy_listbox.Clear()
        for p in self.policy_list:
            policy_discription = p.get_policy_discription()
            self.policy_listbox.Append(policy_discription)

    def on_policy_listbox_doubleclick(self, event):
        index = self.policy_listbox.GetSelection()
        plcy = self.policy_list[index]
        dlg = PolicyDialog(self)
        dlg.title_box.SetValue(plcy.title)
        dlg.message_box.Enable(True)
        dlg.message_box.SetValue(plcy.message)
        dlg.time_ctrl.Enable(True)
        dlg.time_ctrl.SetWxDateTime(wx.pydate2wxdate(plcy.date))
        dlg.calen_ctrl.Enable(True)
        dlg.calen_ctrl.SetDate(wx.pydate2wxdate(plcy.date))
        dlg.periods_combo.Enable(True)
        dlg.periods_combo.SetValue(plcy.period)
        dlg.message_type_combo.Enable(True)
        dlg.message_type_combo.SetValue(plcy.message_type)
        dlg.ok_button.Enable(True)
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            plcy.title = dlg.title_box.GetValue()
            plcy.message = dlg.message_box.GetValue()
            plcy.s_time = dlg.time_ctrl.GetValue()
            if (dlg.calen_ctrl.GetDate() != plcy.date) or (dlg.time_ctrl.GetValue(as_wxDateTime=True) != plcy.date):
                t_time = dlg.time_ctrl.GetValue(as_wxDateTime=True)
                date = dlg.calen_ctrl.GetDate()
                # construct the execution datetime for the reminder
                plcy.date = du.splice_wxDate_wxTime(date, t_time)
                self.delete_policy_reminders(plcy)
                self.reminder_list.extend(pl.create_pending_reminders(plcy))
                self.start_reminder_timers_for_this_policy(plcy)
            plcy.period = dlg.periods_combo.GetValue()
            plcy.message_type = dlg.message_type_combo.GetValue()
            self.policy_list[index] = plcy
            self.save_to_xml()
            self.update_policy_box()
            self.show_pending_reminders()
            dlg.Destroy()
        elif ret == wx.ID_CANCEL:
            dlg.Destroy()

    def on_create_policy_btn(self, event):
        dlg = PolicyDialog(self)
        ret = dlg.ShowModal()
        plcy = pl.Policy()
        if ret == wx.ID_OK:
            plcy.title = dlg.title_box.GetValue()
            plcy.message = dlg.message_box.GetValue()
            plcy.s_time = dlg.time_ctrl.GetValue()
            wxtime = dlg.time_ctrl.GetValue(as_wxDateTime=True)
            wxdate = dlg.calen_ctrl.GetDate()
            # make the execution datetime for the reminder
            plcy.date = du.splice_wxDate_wxTime(wxdate, wxtime)
            plcy.period = dlg.periods_combo.GetValue()
            plcy.message_type = dlg.message_type_combo.GetValue()
            self.policy_list.append(plcy)
            self.save_to_xml()
            self.update_policy_box()
            self.reminder_list.extend(pl.create_pending_reminders(plcy))
            self.start_reminder_timers_for_this_policy(plcy)
            self.show_pending_reminders()
            dlg.Destroy()
        elif ret == wx.ID_CANCEL:
            dlg.Destroy()

    def onAboutHtmlDlg(self, event):
        aboutDlg = AboutDlg(None)
        aboutDlg.Show()

    def onAboutDlg(self, event):
        file = open('LICENSE')
        license = file.read()
        info = wx.adv.AboutDialogInfo()
        info.Name = 'Reminder'
        info.Version = '0.1 Beta'
        info.Copyright = '(C) 2018 Victor Gallagher'
        info.Description = wordwrap(
            'This application allow the user to create various types'
            'of repeating reminders through the creation of policies',
            350, wx.ClientDC(self.p_panel))
        info.Developers = ['Victor Gallagher',
                           ' victor.lamont.gallagher @ gmail.com']
        info.License = wordwrap(license, 600, wx.ClientDC(self.p_panel), margin=5)
        wx.adv.AboutBox(info)

    def on_close(self, event):
        self.Destroy()
        self.save_to_xml()
        for plcy in self.policy_list:
            self.delete_policy(plcy)
            self.cancel_all_timers()

if __name__ == '__main__':
    app = wx.App(False)
    appFrame = MainFrame()
    appFrame.Show()
    app.MainLoop()


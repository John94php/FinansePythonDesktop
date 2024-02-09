import getpass
import os
import threading
import json
import wx
import requests
import time


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)
        self.parent = parent
        sizer = wx.BoxSizer(wx.VERTICAL)
        login_label = wx.StaticText(self, label="Podaj email")
        sizer.Add(login_label, 0, wx.ALL | wx.CENTER, 5)
        self.login_field = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        sizer.Add(self.login_field, 0, wx.ALL | wx.CENTER, 5)
        self.password_label = wx.StaticText(self, label="Podaj hasło")
        sizer.Add(self.password_label, 0, wx.ALL | wx.CENTER, 10)
        self.password_field = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        sizer.Add(self.password_field, 0, wx.ALL | wx.CENTER, 5)
        button = wx.Button(self, label="Zaloguj się")
        register_button = wx.Button(self, label="Nie masz konta? Zarejestruj się!")
        button.Bind(wx.EVT_BUTTON, self.onLogin)
        register_button.Bind(wx.EVT_BUTTON, self.onRegister)
        sizer.Add(button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(register_button, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)

    def onRegister(self, event):
        self.parent.showRegisterPanel()
        pass

    def onLogin(self, event):
        login = self.login_field.GetValue()
        password = self.password_field.GetValue()
        response = self.parent.listPanel.checkLogin(login, password)
        if response.status_code == 200:
            print(response)
            self.parent.showListPanel()


        else:
            print(f"Błąd: {response.status_code}")
            print(response)
            wx.MessageBox("Nieprawidłowe dane!", "Ostrzeżenie", wx.OK | wx.ICON_WARNING)
            self.login_field.Clear()
            self.password_field.Clear()


class ListPanel(wx.Panel):
    def __init__(self, parent):
        super(ListPanel, self).__init__(parent, size=(400, 700))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label="Treść głównego panelu")
        sizer.Add(label, 0, wx.ALL | wx.CENTER, 5)
        bottom_panel = wx.Panel(self)
        add_button = wx.Button(bottom_panel, label="Dodaj")
        add_button.Bind(wx.EVT_BUTTON, self.show_add_form)

        settings_button = wx.Button(bottom_panel, label="Ustawienia")
        logout_button = wx.Button(bottom_panel, label="Wyloguj")

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(add_button, 0, wx.ALL, 10)
        sizer.Add(settings_button, 0, wx.ALL, 10)
        sizer.Add(logout_button, 0, wx.ALL, 10)
        bottom_panel.SetSizer(sizer)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddStretchSpacer()
        main_sizer.Add(bottom_panel, 0, wx.EXPAND)
        self.SetSizer(main_sizer)
    def show_add_form(self,event):
        new_form = AddForm()
        new_form.Show()

    def checkLogin(self, login, password):
        busy_info = wx.BusyInfo("Trwa logowanie...")
        url = "https://finanse.xce.pl/login"
        data = {
            'email': login,
            'password': password
        }

        response = requests.post(url, json=data)
        del busy_info
        return response


class AddForm(wx.Frame):
    def __init__(self):
        super(AddForm, self).__init__(None, title="Mój Formularz", size=(400, 300))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Dodaj tutaj elementy formularza

        panel.SetSizer(sizer)
        self.Layout()


class RegisterPanel(wx.Panel):
    def __init__(self, parent):
        super(RegisterPanel, self).__init__(parent, size=(500, 800))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.register_email_label = wx.StaticText(self, label="Podaj adres email")
        sizer.Add(self.register_email_label, 0, wx.ALL | wx.CENTER, 5)
        self.register_email_field = wx.TextCtrl(self)
        sizer.Add(self.register_email_field, 0, wx.ALL | wx.CENTER, 5)
        self.register_username_label = wx.StaticText(self, label="Podaj swój login")
        sizer.Add(self.register_username_label, 0, wx.ALL | wx.CENTER, 5)
        self.register_username_field = wx.TextCtrl(self)
        sizer.Add(self.register_username_field, 0, wx.ALL | wx.CENTER, 5)
        self.register_password_label = wx.StaticText(self, label="Wprowadź hasło")
        sizer.Add(self.register_password_label, 0, wx.ALL | wx.CENTER, 5)
        self.register_password_field = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        sizer.Add(self.register_password_field, 0, wx.ALL | wx.CENTER, 5)
        self.register_password_confirm_label = wx.StaticText(self, label="Wprowadź ponownie hasło")
        sizer.Add(self.register_password_confirm_label, 0, wx.ALL | wx.CENTER, 5)
        self.register_password_confirm_field = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        sizer.Add(self.register_password_confirm_field, 0, wx.ALL | wx.CENTER, 5)
        self.register_button = wx.Button(self, label="Zarejestruj się!")
        self.register_button.Bind(wx.EVT_BUTTON, self.doRegister)
        sizer.Add(self.register_button, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(sizer)

    def doRegister(self, event):
        username = self.register_username_field.GetValue()
        email = self.register_email_field.GetValue()
        password = self.register_password_field.GetValue()
        confirm_password = self.register_password_confirm_field.GetValue()
        data = {
            'password': password,
            'confirm_password': confirm_password,
            'email': email,
            'username': username
        }
        busy_info = wx.BusyInfo("Trwa rejestracja...")
        url = "https://finanse.xce.pl/register"

        response = requests.post(url, json=data)
        if response.status_code == 200:
            data = response.json()
            dane = data['dane']
            print(dane)
        elif response.status_code == 500:
            print(response)
        else:
            print(f"Błąd: {response.status_code}")
            data = response.json()
            dane = data['error']
            wx.MessageBox(dane, "Ostrzeżenie", wx.OK | wx.ICON_WARNING)
        del busy_info


class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(None, title="Finanses", size=(400, 300))
        self.mainPanel = MainPanel(self)
        self.listPanel = ListPanel(self)
        self.registerPanel = RegisterPanel(self)
        self.listPanel.Hide()
        self.registerPanel.Hide()
        self.SetSize(500, 400)

        self.currentPanel = self.mainPanel

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.sizer.Add(self.listPanel, 1, wx.EXPAND)
        self.sizer.Add(self.registerPanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        menuBar = wx.MenuBar()
        quitMenu = wx.Menu()
        exit_item = quitMenu.Append(wx.ID_EXIT, 'Wyjdz\tCtrl+Q', 'Wyjdź z aplikacji')
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        menuBar.Append(quitMenu, '&Menu')
        self.SetMenuBar(menuBar)

    def showListPanel(self):
        self.currentPanel.Hide()
        self.currentPanel = self.listPanel
        self.listPanel.Show()
        self.Layout()

    def showRegisterPanel(self):
        self.currentPanel.Hide()
        self.currentPanel = self.registerPanel
        self.registerPanel.Show()
        self.Layout()

    def on_exit(self, event):
        # Zamknięcie aplikacji
        self.Close()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

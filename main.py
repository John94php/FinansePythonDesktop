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
        self.login_field = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        sizer.Add(self.login_field,0,wx.ALL | wx.CENTER,5)
        self.password_label = wx.StaticText(self, label="Podaj hasło")
        sizer.Add(self.password_label, 0, wx.ALL | wx.CENTER, 10)
        self.password_field =wx.TextCtrl(self, style=wx.TE_PASSWORD)
        sizer.Add(self.password_field,0,wx.ALL | wx.CENTER,5)
        button = wx.Button(self, label="Zaloguj się")
        button.Bind(wx.EVT_BUTTON, self.onLogin)
        sizer.Add(button, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)

    def onLogin(self, event):
        login = self.login_field.GetValue()
        password = self.password_field.GetValue()
        response = self.parent.listPanel.checkLogin(login,password)
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
        super(ListPanel, self).__init__(parent,size=(400,700))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Dodaj widżety do głównego panelu
        label = wx.StaticText(self, label="Treść głównego panelu")
        sizer.Add(label, 0, wx.ALL | wx.CENTER, 5)
        bottom_panel = wx.Panel(self)

        # Dodawanie przycisków do panelu
        start_button = wx.Button(bottom_panel, label="Start")
        settings_button = wx.Button(bottom_panel, label="Ustawienia")

        # Ustawienie layoutu dla przycisków
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(start_button, 0, wx.ALL, 10)
        sizer.Add(settings_button, 0, wx.ALL, 10)
        bottom_panel.SetSizer(sizer)

        # Dodanie panelu do głównego okna
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddStretchSpacer()  # Dodaj elastyczny odstęp na górze
        main_sizer.Add(bottom_panel, 0, wx.EXPAND)
        self.SetSizer(main_sizer)
        


    def checkLogin(self, login,password):
        busy_info = wx.BusyInfo("Trwa logowanie...")
        url = "https://finanse.xce.pl/login"
        data = {
            'email': login,
            'password': password
        }
        
        response = requests.post(url,json=data)
        del busy_info
        return response


class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(None, title="Finanses", size=(400, 300))
        self.mainPanel = MainPanel(self)
        self.listPanel = ListPanel(self)
        self.listPanel.Hide()
        self.SetSize(500, 500)

        self.currentPanel = self.mainPanel

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.sizer.Add(self.listPanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        menuBar = wx.MenuBar()
        quitMenu = wx.Menu()
        exit_item = quitMenu.Append(wx.ID_EXIT, 'Wyjdz\tCtrl+Q', 'Wyjdź z aplikacji')
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        menuBar.Append(quitMenu, '&Menu')

        # Przypisanie paska menu do okna
        self.SetMenuBar(menuBar)

    def showListPanel(self):
        self.currentPanel.Hide()
        self.currentPanel = self.listPanel
        self.listPanel.Show()
        self.Layout()


    def on_exit(self, event):
        # Zamknięcie aplikacji
        self.Close()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

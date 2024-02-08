import getpass
import os
import threading
import json
import wx

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)

        # Tworzymy sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Dodajemy etykietę
        login_label = wx.StaticText(self, label="Podaj login")
        sizer.Add(login_label, 0, wx.ALL | wx.CENTER, 5)
        self.login_field = wx.TextCtrl(self)
        sizer.Add(self.login_field,0,wx.ALL | wx.CENTER,5)
        self.password_label = wx.StaticText(self, label="Podaj hasło")
        sizer.Add(self.password_label, 0, wx.ALL | wx.CENTER, 10)
        self.password_field =wx.TextCtrl(self, style=wx.TE_PASSWORD)
        sizer.Add(self.password_field,0,wx.ALL | wx.CENTER,5)

        
        
        # Dodajemy przycisk
        button = wx.Button(self, label="Zaloguj się")
        button.Bind(wx.EVT_BUTTON, self.onSwitchPanel)
        sizer.Add(button, 0, wx.ALL | wx.CENTER, 5)

        # Ustawiamy sizer
        self.SetSizer(sizer)

    def onSwitchPanel(self, event):
        login = self.login_field.GetValue()
        password = self.password_field.GetValue()
        self.GetParent().listPanel.updateWithSelectedRoles(login,password)
        self.GetParent().showListPanel()


class ListPanel(wx.Panel):
    def __init__(self, parent):
        super(ListPanel, self).__init__(parent)
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

    def updateWithSelectedRoles(self, login,password):
        print(f"Login: {login}, Hasło: {password}")

        pass



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

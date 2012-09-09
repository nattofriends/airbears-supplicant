"""UI crap."""

import auth
from log import log, unlock

import wx, sys, os, ctypes, threading

if sys.platform == "win32":
    import win32api
if sys.platform == "darwin":
    from Foundation import NSAutoreleasePool

app = None

TRAY_TOOLTIP = 'AirBears Supplicant'
TRAY_ICON = 'assets/tag.png'

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id = item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, dialog):
        super(TaskBarIcon, self).__init__()

        # Under Darwin we have no such trickery such as obtain a handle to our own module. Instead just bundle the icon (temporary).
        if os.path.exists(TRAY_ICON):
            self.SetIcon(wx.IconFromBitmap(wx.Bitmap(TRAY_ICON)), TRAY_TOOLTIP)
        # So normally I would just set data_file properly in build_darwin, but for some reason trying to create a path (assets/) in the bundle makes py2app throw a fit. This should be fixed, preferably by querying the bundle's icns.
        elif sys.platform == "darwin":
            self.SetIcon(wx.IconFromBitmap(wx.Bitmap(os.path.basename(TRAY_ICON))))
        else: # set from executable
            self.SetIcon(wx.Icon(win32api.GetModuleFileName(win32api.GetModuleHandle(None)), wx.BITMAP_TYPE_ICO), TRAY_TOOLTIP)

        self.dialog = dialog
        # self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Change Credentials', self.onShowChangeCredentials)
        create_menu_item(menu, 'Exit', self.onExit)
        return menu
    def onShowChangeCredentials(self, event):
        self.dialog.Show()
        self.dialog.Raise() # They don't automatically go to the front in OSX for some reason
    def onExit(self, event):
        wx.CallAfter(self.Destroy)
    def notice(self, text):
        self.ShowBalloon(title = TRAY_TOOLTIP, text = text, msec = 1000, flags = wx.ICON_INFORMATION)
    def Destroy(self):
        super(TaskBarIcon, self).Destroy()
        # ctypes.windll.user32.PostQuitMessage(0)
        # I should be posting WM_QUIT to ourselves for pythoncom to give up and go home. But PostQuitMessage can be run only from the main thread. So we are SOL, and end ourselves forcefully.
        # Unlock the lockfile first.
        log("Exiting...")
        unlock()
        os._exit(0)

class CalNetPasswordDialog(wx.Frame):
    TITLE = "CalNet Authentication"
    STATUS_DELAY = 1.5
    
    def __init__(self, parent):
        super(CalNetPasswordDialog, self).__init__(parent, title = self.TITLE, style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX, size = (450, 150))
        
        if os.path.exists(TRAY_ICON):
            self.SetIcon(wx.IconFromBitmap(wx.Bitmap(TRAY_ICON)))
        elif sys.platform == "darwin":
            self.SetIcon(wx.IconFromBitmap(wx.Bitmap(os.path.basename(TRAY_ICON))))
        else: # set from executable
            self.SetIcon(wx.Icon(win32api.GetModuleFileName(win32api.GetModuleHandle(None)), wx.BITMAP_TYPE_ICO))
        
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        self.Bind(wx.EVT_CLOSE, self.onDontClose)
        EVT_RESULT(self, self.onAuthCheckDone)
        
        credentials = auth.read_auth() # But not all of them!
        # Some error checking should be done here to silently use empty string if something happened on our way here
        
        panel = wx.Panel(self)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(3, 2, 9, 25)
        
        user_label = wx.StaticText(panel, label = "CalNet ID")
        pass_label = wx.StaticText(panel, label = "Passphrase")
        
        self.username = wx.TextCtrl(panel, style = wx.TE_PROCESS_ENTER, value = credentials[0] if credentials is not None else "")
        self.password = wx.TextCtrl(panel, style = wx.TE_PROCESS_ENTER | wx.TE_PASSWORD)
        
        grid.AddMany(
            [(user_label), (self.username, 1, wx.EXPAND),
             (pass_label), (self.password, 1, wx.EXPAND)])
        
        grid.AddGrowableCol(1, 1)
        vbox.Add(grid, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)
        
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(panel, label = "OK")
        self.button_cancel = wx.Button(panel, label = "Cancel")
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onDontClose)
        self.status = wx.StaticText(panel)
        
        buttons.Add(self.button_ok, flag = wx.ALL, border = 1)
        buttons.Add(self.button_cancel, flag = wx.ALL, border = 1)
        buttons.Add(self.status, flag = wx.ALL, border = 6)
        
        vbox.Add(buttons, proportion = 1, flag = wx.LEFT | wx.RIGHT | wx.EXPAND, border = 10)
        
        panel.SetSizer(vbox)
        
        self.Centre()
        if credentials is None:
            self.Show()
            self.Raise()
        
    def startStatusTimer(self):
        def after():
            pool = NSAutoreleasePool.alloc().init()
            self.status.SetLabel("")
            self.status.SetForegroundColour((0, 0, 0))
            del pool
        threading.Timer(self.STATUS_DELAY, after).start() # Hope they don't re-enter too fast!
        
    # http://wiki.wxpython.org/LongRunningTasks
        
    def onEnter(self, event):
        username = self.username.GetValue()
        password = self.password.GetValue()
        
        if username == "":
            self.status.SetForegroundColour((255, 0, 0))
            self.status.SetLabel("No username entered")
            self.startStatusTimer()
        elif password == "": # If they have neither entered they must be pretty dumb
            self.status.SetForegroundColour((255, 0, 0))
            self.status.SetLabel("No password entered")
            self.startStatusTimer()
        else:
            self.status.SetLabel("Checking...")
            # AuthWorker(self, username, password)
            self.button_ok.Disable()
            self.button_cancel.Disable()
            threading.Thread(target = self.check_auth, args = (username, password)).start()
            
    def onAuthCheckDone(self, event):
        # Main thread -- worker thread posted event back to us
        self.button_ok.Enable()
        self.button_cancel.Enable()
        if event.data[0] == True: # Authenticated successfully
            # We're done, let's get out of here
            auth.write_auth(event.data[1], event.data[2])
            self.status.SetLabel("Success!")
            def hideAndClear():
                # Will be run from worker thread, create own NSAutoreleasePool
                pool = NSAutoreleasePool.alloc().init()
                self.password.SetValue("")
                self.status.SetLabel("")
                self.Hide()
                del pool
            threading.Timer(self.STATUS_DELAY, hideAndClear).start()
        else:
            self.status.SetForegroundColour((255, 0, 0))
            self.status.SetLabel("Bad Calnet ID/passphrase")
        
    def onDontClose(self, event):
        # TextCtrl contents should be cleared now
        self.Hide()
    
    def check_auth(self, username, password):
        result = auth.authenticate(username, password, cas_no_redir = True)
        wx.PostEvent(self, ResultEvent((result, username, password)))

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
         
def init():
    # Don't need to allocate NSAutoreleasePool here, we are on main thread and it was done for us on import
    global app
    app = wx.App()
    dialog = CalNetPasswordDialog(None)
    tb = TaskBarIcon(dialog)
    return tb
    
def start():
    log("Initializing UI")
    app.MainLoop()

if __name__ == '__main__':
    init()
    start()
    
import my_finance as finance
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import _thread as thread
import wx

ID_EVENT_REFRESH = 9999 # 更新事件的ID

class StockFrame(wx.Frame):

    option_list = {'open':True, 'close':True, 'high':False, 'low':False, 'volume':False} # 选择框

    def __init__(self, title):
        wx.Frame.__init__(self, None, title = title, size = (430,600))

        self.CreateStatusBar() # 在框架底部创建一个状态栏,显得比较好看

        menuBar = wx.MenuBar() # 创建一个菜单栏
        filemenu = wx.Menu() # 构造一个菜单对象
        menuBar.Append(filemenu, '&File') # 添加菜单项
        toolmenu = wx.Menu()
        menuBar.Append(toolmenu, '&Tool')

        menuRefresh = filemenu.Append(ID_EVENT_REFRESH, '&Refresh', 'Refresh the price') # 添加菜单选项
        self.Bind(wx.EVT_MENU, self.OnRefresh, menuRefresh) # 绑定菜单事件，如果点击Refresh就会执行OnRefresh函数
        menuQuit = filemenu.Append(wx.ID_EXIT, '&Quit', 'Terminate the program')
        self.Bind(wx.EVT_MENU, self.OnQuit, menuQuit)
        self.SetMenuBar(menuBar)

        panel = wx.Panel(self) # 创建一个Panel对象

        # 创建布局
        codeSizer = wx.BoxSizer(wx.HORIZONTAL) # 水平布局
        labelText = wx.StaticText(panel, label = 'Stock Code:') # 这是一个静态文本
        codeSizer.Add(labelText, 0, wx.ALIGN_BOTTOM)
        codeText = wx.TextCtrl(panel, value = 'BA', style = wx.TE_PROCESS_ENTER) # 这是一个可输入的文本框，默认值为BA
        self.Bind(wx.EVT_TEXT_ENTER, self.OnTextSubmitted, codeText) # 文本框与Enter键绑定，当按下Enter时，执行OnTextSubmitted函数
        codeSizer.Add(codeText)

        optionSizer = wx.BoxSizer(wx.HORIZONTAL) # 水平布局
        for key, value in self.option_list.items():
            checkBox = wx.CheckBox(panel, label = key.title()) # 这是一个复选框
            checkBox.SetValue(value) # 根据value确定是否勾选
            self.Bind(wx.EVT_CHECKBOX, self.OnChecked)
            optionSizer.Add(checkBox)

        self.list = wx.ListCtrl(panel, wx.NewId(), style = wx.LC_REPORT) # 创建一个列表
        self.createHeader() # 创建列表的头部
        # 加载初始界面，在列表第一行显示loading，pos是第一行的index
        pos = self.list.InsertItem(0,'--')
        self.list.SetItem(pos, 1, 'loading...')
        self.list.SetItem(pos, 2, '--')
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClick, self.list) # 列表与双击事件绑定

        ctrlSizer = wx.BoxSizer(wx.HORIZONTAL) # 水平布局
        ctrlSizer.Add((10, 10))
        buttonQuit = wx.Button(panel, -1, 'Quit')
        self.Bind(wx.EVT_BUTTON, self.OnQuit, buttonQuit)
        ctrlSizer.Add(buttonQuit,1)
        buttonRefesh = wx.Button(panel, -1, 'Refresh')
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, buttonRefesh)
        ctrlSizer.Add(buttonRefesh, 1, wx.LEFT|wx.BOTTOM)

        sizer = wx.BoxSizer(wx.VERTICAL) # 垂直布局
        sizer.Add(codeSizer, 0, wx.ALL, 5)
        sizer.Add(optionSizer, 0, wx.ALL, 5)
        sizer.Add(self.list, -1,wx.ALL|wx.EXPAND, 5)
        sizer.Add(ctrlSizer, 0, wx.ALIGN_BOTTOM)

        panel.SetSizerAndFit(sizer)
        self.Center()
        self.OnRefresh(None)


    def createHeader(self):
        """
        创建列表头，第一列：symbol，第二列：name，第三列：lasttrade
        """
        self.list.InsertColumn(0, 'Symbol')
        self.list.InsertColumn(1,'name')
        self.list.InsertColumn(2,'LastTrade')

    def setData(self,data):
        """设置列表内的数据"""
        self.list.ClearAll()
        self.createHeader()
        pos = 0
        for row in data:
            pos = self.list.InsertItem(pos+1, row['code'])
            self.list.SetItem(pos, 1, row['name'])
            self.list.SetColumnWidth(1,-1)
            self.list.SetItem(pos, 2, str(row['price']))
            if pos%2 == 0:
                self.list.SetItemBackgroundColour(pos, (134,225,249))

    def PlotData(self, code):
        """画图"""
        quotes = finance.retrieve_quotes_historical(code)
        fields = ['date','open','close','high','low','volume']
        dates = []
        for i in range(0, len(quotes)):
            x = dt.datetime.utcfromtimestamp(int(quotes[i]['date']))
            y = dt.datetime.strftime(x, '%Y-%m-%d')
            dates.append(y)

        quotesdf = pd.DataFrame(quotes, index=dates, columns=fields)

        fields_to_drop = ['date']
        for key, value in self.option_list.items():
            if not value:
                fields_to_drop.append(key)

        quotesdf = quotesdf.drop(fields_to_drop,axis = 1)
        quotesdf.plot()
        plt.show()

    def OnDoubleClick(self,event):
        self.PlotData(event.GetText())

    def OnTextSubmitted(self,event):
        self.PlotData(event.GetString())

    def OnChecked(self,event):
        """
        复选框点击函数，获取复选框的文本内容，并将option_list中对于的value设为True
        """
        checkBox = event.GetEventObject()
        text = checkBox.GetLabel().lower()
        self.option_list[text] = checkBox.GetValue()

    def OnQuit(self,event):
        """退出"""
        self.Close()
        self.Destroy()

    def OnRefresh(self,event):
        """刷新"""
        thread.start_new_thread(self.retrieve_quotes,())

    def retrieve_quotes(self):
        """获取股票数据"""
        data = finance.retrieve_dji_list()
        if data:
            self.setData(data)
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App(False)
    top = StockFrame('Dow Jones Industrial Average(^DJI)')
    top.Show(True)
    app.MainLoop()

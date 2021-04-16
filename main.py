import wx
from wx.core import CommandEvent, Frame, GBPosition, ID_ANY, Image, Panel
import os 
import time
from pyaudio import PyAudio
import wave



def get_file(file_name):
    return os.path.dirname(os.path.abspath(__file__)) + file_name

class MessageBox(wx.Frame):
    def __init__( self, parent, title, task_name ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.SIMPLE_BORDER|wx.TRANSPARENT_WINDOW )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 57, 57, 57 ) )
        

        sizer = wx.GridBagSizer( 0, 0 )
        sizer.SetFlexibleDirection( wx.BOTH )
        sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.on_time = wx.StaticText( self, wx.ID_ANY, u"时间到啦!", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.on_time.Wrap( -1 )

        self.on_time.SetFont( wx.Font( 20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI" ) )
        self.on_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )

        sizer.Add( self.on_time, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.task = wx.StaticText( self, wx.ID_ANY, u"任务:{}".format(task_name), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.task.Wrap( -1 )

        self.task.SetFont( wx.Font( 13, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI Light" ) )
        self.task.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )

        sizer.Add( self.task, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.ten_minutes = wx.Button( self, wx.ID_ANY, u"延长十分钟", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ten_minutes.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI Light" ) )

        sizer.Add( self.ten_minutes, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.yes = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.yes.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI Light" ) )

        sizer.Add( self.yes, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


        self.SetSizer( sizer )
        self.Layout()
        sizer.Fit( self )

        # Connect Events
        self.ten_minutes.Bind( wx.EVT_BUTTON, self.ten_minutes_ )
        self.yes.Bind( wx.EVT_BUTTON, self.on_close )

    def __del__( self ):
        pass


        # Virtual event handlers, overide them in your derived class
    def ten_minutes_( self, event ):
        self.Destroy()
        return False

    def on_close( self, event ):
        self.Destroy()
        return True
        
class Play():
    def __init__(self) -> None:
        pass
    def play_music(self, file, judge_func, *args, **kwargs):
        chunk=1024  #2014kb
        wf=wave.open(file,'rb')
        self.p=PyAudio()
        self.stream=self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
    
        data = wf.readframes(chunk)  # 读取数据
            
        while True:
            data=wf.readframes(chunk)
            if data=="" or eval(judge_func(*args, **kwargs)):
                break
            self.stream.write(data)
        self.stream.stop_stream()   # 停止数据流
        self.stream.close()
        self.p.terminate()  # 关闭 PyAudio
        print('play_music函数结束！')

 


class TransparentText(wx.StaticText):#继承了wx.Statictext的类，并对相应的方法进行重写;
    def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TRANSPARENT_WINDOW, name='transparenttext'):
        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_paint(self, event):#重写on_paint可以对控件进行重写重新构造形状 
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)
        font_face = self.GetFont()
        font_color = self.GetForegroundColour()
        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)
        

    def on_size(self, event):
        self.Refresh()
        event.Skip()
        


        
        
        
class MyPannel ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1100,630 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )
        self.bitmap = wx.StaticBitmap(self, -1, self.img_backgroud(1100, 600, get_file("\\img\\background.jpg")), (0, 0))

        self.gbSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.task_name = []
        self.hours = []
        self.minutes = []
        self.plan_object_lst = {}
        self.plan_lst = {"date_timer":{}, "count_down":{}}

        self.gbSizer2 = wx.GridBagSizer( 0, 0 )
        self.gbSizer2.SetFlexibleDirection( wx.BOTH )
        self.gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.time_panel = wx.Panel(self.bitmap, size=(1100, 150))
        self.time_panel.SetBackgroundColour("white")
        
        self.time_sizer = wx.BoxSizer()

        self.morning_or_night = wx.StaticText( self.time_panel, wx.ID_ANY, label="早上好")
        self.morning_or_night.SetFont( wx.Font( 80, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI" ) )
        self.morning_or_night.SetForegroundColour("black")

        self.time_sizer.Add(self.morning_or_night)

        self.time_text = wx.StaticText( self.time_panel, wx.ID_ANY, label="北京时间:                                       ")
        self.time_sizer.Add(self.time_text)
        self.time_text.Wrap( -1 )
        self.time_text.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI" ))
        self.time_text.SetForegroundColour("black")


        #self.gbSizer2.Add( self.time_text, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_BOTTOM, 5 )
        
        
        
        #self.gbSizer2.Add( self.morning_or_night, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.m_bpButton1 = wx.BitmapButton( self.time_panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

        self.m_bpButton1.SetBitmap( wx.Bitmap(get_file("\\img\\create.png"), wx.BITMAP_TYPE_ANY ) )
        self.time_sizer.Add(self.m_bpButton1)

        self.time_panel.SetSizer(self.time_sizer)
        

        self.gbSizer2.Add(self.time_panel, wx.GBPosition(0, 0), wx.GBSpan( 1, 1 ), wx.BOTTOM, 25)
        #self.gbSizer2.Add( self.m_bpButton1, wx.GBPosition( 0, 5 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_BOTTOM, 5 )

        
        self.plan_sizer = wx.GridBagSizer( 0, 0 )
        self.plan_sizer.SetFlexibleDirection(wx.BOTH)
        
        self.plan_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
                
        self.plan_sizer.Add( self.plan(), wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
        
        self.gbSizer2.Add( self.plan_sizer, wx.GBPosition( 1, 0 ), wx.GBSpan( 18, 45 ), wx.EXPAND, 5 )


        self.gbSizer1.Add( self.gbSizer2, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( self.gbSizer1 )
        self.Layout()
        
        
        
        # Connect Events
        self.timer = wx.Timer(self)#创建定时器
        self.Bind(wx.EVT_TIMER, self.change_time, self.timer)#绑定一个定时器事件
        self.timer.Start(1000)#设定时间间隔

        self.m_bpButton1.Bind( wx.EVT_BUTTON, lambda e: self.add_plan(e, "self.plan()"))
        
        self.Bind(wx.EVT_TIMER,self.change_time)

        self.timer_two = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.plan_timer, self.timer_two)
        self.timer_two.Start(2000)
        
        
        

    def img_backgroud(self, hight, weith, file):
        image_file = file
        to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        img = to_bmp_image.ConvertToImage()
        tp = img.Scale(hight, weith).ConvertToBitmap()
        return tp
        
    def plan(self):
        self.plan_sizer_all = wx.GridBagSizer(0, 0)
        
        self.plan_sizer1 = wx.Panel(self.bitmap)
        
        self.gbSizer = wx.GridBagSizer( 0, 0 )
        self.gbSizer.SetFlexibleDirection( wx.BOTH )
        self.gbSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        
        #self.plan_sizer1 = wx.Panel(self.bitmap)
        
        self.task = wx.StaticText( self.plan_sizer1, wx.ID_ANY, u"任务:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.task.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI" ) )
        self.task.Wrap( -1 )
        
        self.gbSizer.Add( self.task, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)

        self.input_task = wx.TextCtrl( self.plan_sizer1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.input_task.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI" ) )
        self.gbSizer.Add( self.input_task, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 3 ), wx.ALL, 5 )

        self.time = wx.StaticText( self.plan_sizer1, wx.ID_ANY, u"时间:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.time.Wrap( -1 )
        

        self.gbSizer.Add( self.time, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.time_choice_hourChoices = [ u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16", u"17", u"18", u"19", u"20", u"21", u"22", u"23", u"24" ]
        self.time_choice_hour = wx.Choice( self.plan_sizer1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 50,-1 ), self.time_choice_hourChoices, 0 )
        self.time_choice_hour.SetSelection( 0 )
        self.gbSizer.Add( self.time_choice_hour, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.time_choice_minuteChoices = [str(i) for i in range(0, 60)]
        self.time_choice_minute = wx.Choice( self.plan_sizer1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 50,-1 ), self.time_choice_minuteChoices, 0 )
        self.time_choice_minute.SetSelection( 0 )
        self.gbSizer.Add( self.time_choice_minute, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.maohao = wx.StaticText( self.plan_sizer1, wx.ID_ANY, u":", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.maohao.Wrap( -1 )

        self.gbSizer.Add( self.maohao, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.yes = wx.Button( self.plan_sizer1, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        self.gbSizer.Add( self.yes, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )
        
        #self.plan_sizer1.Add( gbSizer, wx.GBPosition(0, 0))
        #self.plan_sizer1.SetSizer(self.plan_sizer1)
        self.plan_sizer1.SetSizer(self.gbSizer)
        #self.Layout()

        self.yes.Bind( wx.EVT_BUTTON, self.get_plan_input )
        self.task_name.append("")
        self.hours.append("")
        self.minutes.append("")

        #simplify_ui
        self.plan_sizer2 = wx.Panel(self.bitmap)
        
        self.simplify_gbSizer = wx.GridBagSizer( 0, 0 )
        self.simplify_gbSizer.SetFlexibleDirection( wx.BOTH )
        self.simplify_gbSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        
        
        self.task_ = wx.StaticText( self.plan_sizer2, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.task_.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI" ) )
        self.task_.Wrap( -1 )
        
        self.simplify_gbSizer.Add( self.task_, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)

        self.time_ = wx.StaticText( self.plan_sizer2, wx.ID_ANY, u"时间:    时    分", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.time_.Wrap( -1 )
        self.time_.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI" ) )

        self.simplify_gbSizer.Add( self.time_, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.plan_sizer2.SetSizerAndFit(self.simplify_gbSizer)
        #self.simplify_gbSizer.Hide(self.simplify_gbSizer)

        
        self.plan_sizer_all.Add(self.plan_sizer1, wx.GBPosition(0, 0), wx.GBSpan( 1, 1 ), wx.ALL, 5)
        self.plan_sizer_all.Add(self.plan_sizer2, wx.GBPosition(0, 1), wx.GBSpan( 1, 1 ), wx.ALL, 5)
        self.plan_sizer_all.Hide(self.plan_sizer2)
        #self.plan_sizer.Add( plan_sizer1, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
        self.gbSizer2.Layout()
    
        #self.plan_object_lst[self.task] = (self.plan_sizer_all)
        return self.plan_sizer_all
        

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def add_plan( self, event, win ):
        event.Skip()
        
    def change_time(self, event):
        event.Skip()

    def get_plan_input(self, event):
        event.Skip()
    
    def plan_timer(self, event):
        event.Skip()

        


class Method(MyPannel):
    def __init__(self, parent):
        super().__init__(parent)
        self.plan_xy = (0, 1)
        self.time_lst = []
        print(self.time_lst)

    
    def get_plan_input(self, event):
        if self.simplify_planui() == False:
            return False
        self.time_lst.append((self.task_name[-1], "{}:{}".format(self.hours[-1], self.minutes[-1]) 
                                if len(str(self.minutes[-1])) == 2 and len(str(self.hours[-1])) == 2
                                else ("{}:0{}".format(self.hours[-1], self.minutes[-1])
                                        if len(str(self.hours[-1])) == 2 and len(str(self.minutes[-1])) == 1
                                        else ("0{}:0{}".format(self.hours[-1], self.minutes[-1])
                                                if len(str(self.hours[-1])) == 1 and len(str(self.minutes[-1])) == 1
                                                else "0{}:{}".format(self.hours[-1], self.minutes[-1])) ) ))

        self.time_lst = sorted(self.time_lst, key=lambda x:x[1])
        print(self.time_lst)
        return True
    
    def __get_plan(self, index = -1):
        self.task_name[index] = self.input_task.GetValue()
        self.hours[index] = self.time_choice_hour.GetStringSelection()
        self.minutes[index] = (self.time_choice_minute.GetStringSelection())
        
        

    def add_plan(self, event, win):
        self.__get_plan()

        if self.__judge_input_plan_and_handle() != True:
            return False
        self.__show_plan_sizer(self.task_name[-1], self.hours[-1], self.minutes[-1])
        
            
        b = False
        for y in range(0, 4, 2):
            for x in range(1, 10, 2):
                if y < self.plan_xy[0]:
                    continue
                elif x <= self.plan_xy[1] and y <= self.plan_xy[0]:
                    continue
                self.plan_sizer.Add( eval(win) if type(win) == str else win, wx.GBPosition( y, x ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
                b = True
                break
            if b:
                self.plan_xy = (y, x)
                break
  
        self.Layout()
        self.Refresh()
        return True
        
        
    def change_time(self, event):
        self.time_text.SetLabel("北京时间:"+str(time.strftime('%Y-%m-%d %H:%M:%S')))

        mytime = time.localtime()
        self.morning_or_night.SetLabel("晚上好" if 18 < mytime.tm_hour < 23 else ("上午好" if 0 < mytime.tm_hour < 12 else "下午好"))
    def __judge_input_plan_and_handle(self):
        '''
        return: false-->small task, true-->a common plan, none-->empty task name
        '''
        tp = self.__wheather_task_empty_or_small(-1)
        if tp == True:
            dlg = wx.MessageDialog(None, u"请输入任务名字", u"提醒", wx.YES_NO | wx.ICON_QUESTION)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        elif tp == None:
            return True
        elif tp == False:
            dlg = wx.MessageDialog(None, u"输入的时间已经过时哦", u"提醒", wx.YES_NO | wx.ICON_QUESTION)
            dlg.ShowModal()
            dlg.Destroy()
            return None
        else: pass
    def __wheather_task_empty_or_small(self, index= -1) ->bool:
        '''
        index :plan index
        return: false-->small task, true-->empty task name, none-->a common plan
        '''
        if self.task_name[index] == "" or self.task_name == []:
            return True
        elif self.hours[-1] < time.strftime("%H") or (self.minutes[-1] < time.strftime("%M") and self.hours[-1] == time.strftime("%H")):
            return False
        else:
            self.plan_object_lst[self.task_name[-1]] = self.plan_sizer_all
            return None

    def simplify_planui(self):
        self.__get_plan()
        if self.__judge_input_plan_and_handle():
            self.__show_plan_sizer(self.task_name[-1], self.hours[-1], self.minutes[-1])
            self.Layout()

    def __show_plan_sizer(self, task_name, time_hour, time_minute):
        self.plan_sizer_all.Hide(self.plan_sizer1)
        self.plan_sizer_all.Show(self.plan_sizer2)
        self.time_.SetLabel("时间: {}时{}分".format(time_hour, time_minute))
        self.task_.SetLabel("{}".format(task_name))
        
        self.plan_sizer_all.Layout()



    def plan_timer(self, event):
        #while True:
            
        print(self.time_lst)

        try:
            if str(time.strftime("%H:%M")) > self.time_lst[0][1]:
                del self.time_lst[0][1]
            print(str(time.strftime("%H:%M")))
            if str(time.strftime("%H:%M")) == self.time_lst[0][1]:
                dlg = wx.MessageDialog(None, u"任务:{}".format(self.time_lst[0][0]), u"时间到啦!", wx.YES_NO | wx.ICON_QUESTION)
                play_music = Play()
                play_music.play_music(get_file("\\audio\\try.wav"))
                dlg.ShowModal() 
                

                
                #play_music.stop_music()
                
                dlg.Destroy()
                print(str(self.plan_object_lst))

                del self.plan_object_lst[self.time_lst[0][0]]
                del self.time_lst[0]
                self.Update()
                
                
        except IndexError:
            print("indexe")
                
        
       # time.sleep(2)


        
        


if __name__ == "__main__":
    app = wx.App()
    myframe = wx.Frame(None, title = "SYT", size = wx.Size(1100, 630))
    WinUi= Method(myframe)
    myframe.SetTransparent(480)
    myframe.Centre()
    myframe.Show()
    #aaa = MessageBox(None , "hello", "nihao")
    #aaa.Show()
    #t = threading.Thread(target=WinUi.plan_timer)
    #t.start()
    app.MainLoop()

    
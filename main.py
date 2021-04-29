import os
import time
import wx
import wx.aui
from wx.core import Button, ID_ANY
import wx.lib.agw.customtreectrl as customtreectrl


def get_file(file_name):
    '''
    :param file_name: relative file path
    :return: file path
    '''
    return os.path.dirname(os.path.abspath(__file__)) + file_name

class ButtonPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour("red")

class PlanBitmapButton(wx.BitmapButton):
    def __init__(self, parent, file_path, width, height):
        
        plan_icon = wx.Image(file_path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        img = plan_icon.ConvertToImage()
        
        self.plan_icon = img.Scale(width, height).ConvertToBitmap()
        super().__init__(parent, id=wx.ID_ANY, bitmap=self.plan_icon, style=wx.BORDER_NONE)
        self.Bind(wx.EVT_BUTTON, lambda _: self.Refresh())

    def SetBitmapFocus(self, file_path, width, height):
        plan_icon = wx.Image(file_path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        img = plan_icon.ConvertToImage()
        
        bitmap = img.Scale(width, height).ConvertToBitmap()
        super().SetBitmapFocus(bitmap)
        
        
    
class ListPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour("#2a2a2a")
        v_sizer = wx.BoxSizer(wx.VERTICAL)

        self.plan_list_title = wx.StaticText(self, label="我的任务集", style=wx.NO_BORDER)
        self.plan_list_title.SetBackgroundColour("#2a2a2a")
        self.plan_list_title.SetForegroundColour("white")
        self.plan_list_title.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, False, "Microsoft YaHei UI", wx.FONTENCODING_DEFAULT))
        #c_sizer.Add(self.plan_list_title, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
        v_sizer.AddSpacer(20)
        v_sizer.Add(self.plan_list_title, flag=wx.ALIGN_CENTER)
        v_sizer.AddSpacer(20)

        b_panel = wx.Panel(self)
        
        b_panel.SetBackgroundColour("#F0F0F0")

        b_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.create_plan_button = PlanBitmapButton(b_panel, get_file("\\img\\add.png"), 20, 20)
        self.create_plan_button.SetBitmapCurrent(wx.Image(get_file("\\img\\add_focus.png")).Scale(20, 20).ConvertToBitmap())
        
        b_sizer.Add(self.create_plan_button, flag=wx.ALIGN_RIGHT)
        b_panel.SetSizer(b_sizer)
        v_sizer.Add(b_panel, flag=wx.EXPAND)
    

        self.plan_tree = PlanTree(self)
        v_sizer.Add(self.plan_tree, proportion=1,flag=wx.EXPAND)
        self.SetSizer(v_sizer)
        self._init_popup_menu()
        self._init_event()

    def _init_popup_menu(self):
        self.menu = wx.Menu()
        self.menu_id_create_plan = wx.NewIdRef()
        self.menu_id_edit_plan = wx.NewIdRef()
        self.menu_id_delete_plan = wx.NewIdRef()

        self.menu.Append(self.menu_id_create_plan, u'创建任务集')
        #self.menu.Append(self.menu_id_edit_plan, u'编辑任务集')
        self.menu.Append(self.menu_id_delete_plan, u'删除任务集')

    def _init_event(self):
        self.Bind(wx.EVT_CONTEXT_MENU, self._show_popup_menu)
        self.Bind(wx.EVT_MENU, self._create_plan, id=self.menu_id_create_plan)
        #self.Bind(wx.EVT_MENU, self._edit_plan, id=self.menu_id_edit_plan)
        self.Bind(wx.EVT_MENU, self._delete_plan, id=self.menu_id_delete_plan)

        self.create_plan_button.Bind(wx.EVT_BUTTON, self._create_plan)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.create_display_plan)
    def _show_popup_menu(self, _):
        self.PopupMenu(self.menu)

    def create_display_plan(self, event):
        print(event)

    def _create_plan(self, event):
        with PlanDialog(self) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                #item = self.plan_tree.AppendItem(self.plan_tree.GetSelection(), dialog.get_name())
                self.plan_tree.create_plan(dialog.get_name())
    #def _edit_plan(self, event):
        '''with PlanDialog(self, False) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                item = self.plan_tree.AppendItem(self.plan_tree.GetSelection(), dialog.get_name())
                '''
        #pub.sendMessage('notebook.editing')
    def _delete_plan(self, event):
        self.plan_tree.delete_plan()
    

class TitlePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.time_sizer = wx.BoxSizer()
        
        self.morning_or_night = wx.StaticText( self, wx.ID_ANY, label="早上好")
        self.morning_or_night.SetFont( wx.Font( 80, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI" ) )
        self.morning_or_night.SetForegroundColour("black")

        self.time_sizer.Add(self.morning_or_night)

        self.time_text = wx.StaticText( self, wx.ID_ANY, label="北京时间:                                       ")
        self.time_sizer.Add(self.time_text)
        
        self.time_text.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI" ))
        self.time_text.SetForegroundColour("black")
        self.SetSizer(self.time_sizer)

        self.time_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.change_time, self.time_timer)#绑定一个定时器事件
        self.time_timer.Start(1000)#设定时间间隔

    def change_time(self, event):
        self.time_text.SetLabel("北京时间:"+str(time.strftime('%Y-%m-%d %H:%M:%S')))

        mytime = time.localtime()
        self.morning_or_night.SetLabel("晚上好" if 18 < mytime.tm_hour < 23 else ("上午好" if 0 < mytime.tm_hour < 12 else "下午好"))


class PlanPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour("#E5E5E5")
        self.main_sizer = wx.GridBagSizer()
        
        self.SetSizer(self.main_sizer)
        self.create_plan_manager("plan1")

    def create_plan_manager(self, title):
        self.plan_manager = PlanManager(self, title)
        self.main_sizer.Add(self.plan_manager, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)

class PlanManager(wx.Panel):
    def __init__(self, parent, title):
        super().__init__(parent, size=(250, -1))
        self.SetBackgroundColour("#FFFFFF")
        self._init_plan_ui(title)
        
    def _init_plan_ui(self, title):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.title = wx.StaticText(self, ID_ANY, title)
        self.title.SetFont(wx.Font(17, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei UI"))
        self.main_sizer.Add(self.title, flag=wx.ALL|wx.ALIGN_LEFT, border=10)
        self.main_sizer.AddSpacer(10)

        self.SetSizer(self.main_sizer)
        self._user_create_plan()
    
    def _user_create_plan(self):
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.child_plan_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.child_plan_panel.SetBackgroundColour("#E5E5E5")

        sizer = wx.GridBagSizer( 0, 0 )
        sizer.SetFlexibleDirection( wx.BOTH )
        sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.input_name = wx.TextCtrl( self.child_plan_panel, wx.ID_ANY, u"plan name", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
        self.input_name.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        sizer.Add( self.input_name, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 5 ), wx.ALL, 5 )

        self.input_hours = wx.SpinCtrl( self.child_plan_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 1, 24, 1 )
        sizer.Add( self.input_hours, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.m_staticText2 = wx.StaticText( self.child_plan_panel, wx.ID_ANY, u":", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        sizer.Add( self.m_staticText2, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.input_minutes = wx.SpinCtrl( self.child_plan_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 1, 59, 1 )
        sizer.Add( self.input_minutes, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.m_bpButton1 = wx.BitmapButton( self.child_plan_panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE )

        self.m_bpButton1.SetBitmap( wx.Bitmap( get_file("\\img\\yes.png"), wx.BITMAP_TYPE_PNG ).ConvertToImage().Scale(20, 20).ConvertToBitmap() )
        print(get_file("\\img\\yes_focus.png"))
        self.m_bpButton1.SetBitmapCurrent(wx.Bitmap( get_file("\\img\\yes_focus.png"), wx.BITMAP_TYPE_PNG ).ConvertToImage().Scale(20, 20).ConvertToBitmap())

        sizer.Add( self.m_bpButton1, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.m_bpButton2 = wx.BitmapButton( self.child_plan_panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE )

        self.m_bpButton2.SetBitmap( wx.Bitmap( get_file("\\img\\more.png"), wx.BITMAP_TYPE_PNG ).ConvertToImage().Scale(20, 20).ConvertToBitmap() )
        self.m_bpButton2.SetBitmapCurrent(wx.Bitmap( get_file("\\img\\more_focus.png"), wx.BITMAP_TYPE_PNG ).ConvertToImage().Scale(20, 20).ConvertToBitmap())
        sizer.Add( self.m_bpButton2, wx.GBPosition( 1, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


        self.child_plan_panel.SetSizer( sizer )
        self.child_plan_panel.Layout()
        sizer.Fit( self.child_plan_panel )
        bSizer2.Add( self.child_plan_panel, 1, wx.EXPAND |wx.ALL, 0 )


        #self.SetSizer( bSizer2 )
        self.Layout()

        # Connect Events
        self.m_bpButton1.Bind( wx.EVT_BUTTON, self.display_plan and (
            lambda event:self.update_plan_sizer(event, self.m_bpButton1)
            ))
        self.m_bpButton2.Bind(wx.EVT_BUTTON, self.more_plan and (
            lambda event: self.update_plan_sizer(event, self.m_bpButton2)
        ))


        self.main_sizer.Add(self.child_plan_panel, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        
    def display_plan(self, event):
        pass
    
    def more_plan(self, event):
        pass

    def update_plan_sizer(self, event, bt):
        '''refresh the button'''
        bt.Refresh()
        print("refresh the button update_plan_sizer")

class PlanTree(customtreectrl.CustomTreeCtrl):
    def __init__(self, parent):
        super().__init__(parent,agwStyle=customtreectrl.TR_HAS_BUTTONS|customtreectrl.TR_FULL_ROW_HIGHLIGHT|customtreectrl.TR_ELLIPSIZE_LONG_ITEMS|customtreectrl.TR_TOOLTIP_ON_LONG_ITEMS|customtreectrl.TR_NO_LINES)
        self.SetBackgroundColour("#2a2a2a")
        self.SetHilightFocusColour("#8BA0FF")
        self.SetHilightNonFocusColour("#2a2a2a")
        self.SetForegroundColour("#ececec")

        self.EnableSelectionGradient(False)

        panel_font = self.GetFont()
        panel_font.SetPointSize(panel_font.GetPointSize() + 1)
        self.SetFont(panel_font)

        self.SetSpacing(20)
        self.SetIndent(10)

        self.root = self.AddRoot("我的任务集")

        self._load_plan_list({"root1":["dsaf ", "dsaf"], "root2":[1]})

    def create_plan(self, name):
        item = self.AppendItem(self.GetSelection(), name)
        self.DoSelectItem(item)
        

    def delete_plan(self):
        #item = self.AppendItem(self.GetSelection(), self.GetSelection())
        if self.GetSelection() != self.root:
            self.Delete(self.GetSelection())
        else:
            dialog = wx.MessageDialog(self, "无法删除哦~", "无法删除", wx.OK)
            dialog.ShowModal()
    
        
    def _load_plan_list(self, tree_plan_data: dict):
        '''
        :params tree_plan_data: data for trees:
        {root1: [item1, item2...]
         root2: [...]}
        '''
        #root_plan = [i for i in tree_plan_data.keys()]

        for plan_set in tree_plan_data.items():
            root_node = self.AppendItem(self.root, plan_set[0], on_the_right=True)
            for plan_item in plan_set[1]:
                self.AppendItem(root_node, str(plan_item))
                
            
        self.ExpandAll()

class PlanDialog(wx.Dialog):
    def __init__(self, parent, title=None):
        title_ = '新建任务集' if title is None else "编辑任务集"

        super().__init__(parent, title=title_)
        

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        g_sizer = wx.FlexGridSizer(cols=2,gap=(10, 10))
        g_sizer.AddGrowableCol(1)

        g_sizer.Add(wx.StaticText(self, label='名称'))
        self.tc_name = wx.TextCtrl(self, size=(400,-1))
        g_sizer.Add(self.tc_name, flag=wx.EXPAND)

        g_sizer.Add(wx.StaticText(self, label='描述(可选)'))
        self.tc_description = wx.TextCtrl(self, size=(400, 160),style=wx.TE_MULTILINE)
        g_sizer.Add(self.tc_description, flag=wx.EXPAND)

        main_sizer.Add(g_sizer, flag=wx.EXPAND|wx.ALL, border=10)

        btn_sizer = wx.StdDialogButtonSizer()
        btn_sizer.AddButton(wx.Button(self, wx.ID_CANCEL, '取消'))
        ok_button = wx.Button(self, wx.ID_OK, '确定')
        ok_button.SetDefault()

        btn_sizer.AddButton(ok_button)
        btn_sizer.Realize()
        main_sizer.Add(btn_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, border=5)

        '''if title != None:
            self.tc_name.SetValue(title.name)
            self.tc_description.SetValue(title.description)
            self.tc_name.SelectAll()'''

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

        self.CenterOnScreen()
        self.Bind(wx.EVT_BUTTON, self._on_save, id=wx.ID_OK)

    def get_name(self):
        return self.tc_name.GetValue().strip()

    def get_description(self):
        return self.tc_description.GetValue().strip()

    def _on_save(self, e):
        if self.get_name():
            self.EndModal(wx.ID_OK)
class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None)

        self.aui_manager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_TRANSPARENT_HINT)

        self.title_panel = TitlePanel(self)
        self.plan_panel = PlanPanel(self)
        self.button_panel = ButtonPanel(self)
        self.list_panel = ListPanel(self)

        self.aui_manager.AddPane(self.button_panel, self._get_default_pane_info().Left().BestSize(50,-1))
        self.aui_manager.AddPane(self.title_panel, self._get_default_pane_info().Top().BestSize(-1, 200).MinSize(-1, 150))
        self.aui_manager.AddPane(self.plan_panel, self._get_default_pane_info().CenterPane().Position(0).BestSize(800,-1))
        self.aui_manager.AddPane(self.list_panel, self._get_default_pane_info().Left().Row(1).BestSize(600,-1).MinSize(300, -1))
        
        
    

        self.aui_manager.Update()

        self.Maximize(True)
        self.SetMinSize((700, 400))
    def _get_default_pane_info(self):
        return wx.aui.AuiPaneInfo().CaptionVisible(False).PaneBorder(False).CloseButton(False).PinButton(False).Gripper(False)

    def __del__(self):
        self.aui_manager.UnInit()
        

class MyApp(wx.App):
    def OnInit(self):
        MainFrame().Show()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()

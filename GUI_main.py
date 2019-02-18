#!/usr/bin/env python
#
# generated by wxGlade 0.9.1 on Mon Feb 18 11:19:47 2019
#
import wx
import os

from time import sleep

from loadConfig import loadConfig 


import BIOSUP

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class GUI_Window(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GUI_Window.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.allarr = []
        self.config = loadConfig("GUI_config.ini")
        #self.SetSize((400, 300))
        self.AMD_Chq_List = wx.CheckListBox(self, wx.ID_ANY, choices=self.config.AMDallowedchipsets)
        self.Intel_Chq_List = wx.CheckListBox(self, wx.ID_ANY, choices=self.config.INTELallowedchipsets)
        self.Vendor_Chq_List = wx.CheckListBox(self, wx.ID_ANY, choices=self.config.vendor)
        self.Run_Btn = wx.Button(self, wx.ID_ANY, "Run")
        self.Selectall_Btn = wx.Button(self,wx.ID_ANY,"Select All")
        self.useLast_Btn = wx.CheckBox(self,wx.ID_ANY,"Run last config")
        self.Status_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY|wx.TE_MULTILINE)


        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        self.Run_Btn.Bind(wx.EVT_BUTTON, self.Run_Event)
        self.Selectall_Btn.Bind(wx.EVT_BUTTON, self.Select_All_Chq_Box)
        self.useLast_Btn.Bind(wx.EVT_BUTTON, self.Select_Last_Run)

        self.useLast_Btn.SetValue(True)

    def __set_properties(self):
        # begin wxGlade: GUI_Window.__set_properties
        self.SetTitle("BIOSUP")
        self.Status_text_ctrl.SetMinSize((-1,-1))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: GUI_Window.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(3, 3, 0, 0)
        sizer_4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Vendors"), wx.VERTICAL)
        sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Intel Chipsets"), wx.VERTICAL)
        sizer_2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "AMD Chipsets"), wx.VERTICAL)

        sizer_2.Add(self.AMD_Chq_List, 0, 0, 0)
        grid_sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_3.Add(self.Intel_Chq_List, 0, 0, 0)
        grid_sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_4.Add(self.Vendor_Chq_List, 0, 0, 0)
        grid_sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

        grid_sizer_1.Add(self.Selectall_Btn, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.useLast_Btn, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.Run_Btn, 0, wx.ALIGN_RIGHT, 0)

        sizer_1.Add(grid_sizer_1, 0, 0, 0)
        sizer_1.Add(self.Status_text_ctrl, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
        self.Status_text_ctrl.AppendText("Waiting for user input...\n")
        
    def Run_Event(self, evt):
        print("Attempting to run BIOSUP...")
        self.datapath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"\\config.ini"
        if self.Chq_fields():
            with open (self.datapath,"w") as outfile:
                self.Status_text_ctrl.AppendText("Writing config file...\n")
                outfile.write("[SETTINGS]\nclean = t\nFireFox = \nopenBrowser = \n")
                outfile.write("saveState = t\nsleeptimer = 6\nsleepwait = 5\n")
                outfile.write("allowedChipsets = "+", ".join(self.allarr)+"\n")
                outfile.write("allowedChipsetsAddon = [CIM]?\n")
                outfile.write("vendor = "+", ".join(self.Vendor_Chq_List.GetCheckedStrings())+"\n")
                self.Status_text_ctrl.AppendText("Done...\n")
            self.Status_text_ctrl.AppendText("GUI may freeze during running...\n")
            BIOSUP.main()
        elif self.useLast_Btn.IsChecked():
            self.Status_text_ctrl.AppendText("GUI may freeze during running...\n")
            BIOSUP.main()
        else:
            self.Status_text_ctrl.AppendText("Select at least 1 chipset and vendor or tick 'Run last config' \n")
        self.Status_text_ctrl.AppendText("BIOSUP Completed...\n")
    def Chq_fields(self):
        self.allarr = self.AMD_Chq_List.GetCheckedStrings() + self.Intel_Chq_List.GetCheckedStrings()+ self.Vendor_Chq_List.GetCheckedStrings()
        if not len(self.allarr) == 0:    
            return True
        else:
            return False

    def Select_All_Chq_Box(self, evt): 
        print("Selecting all tick boxes")
        self.AMD_Chq_List.SetCheckedStrings(self.config.AMDallowedchipsets)
        self.Intel_Chq_List.SetCheckedStrings(self.config.INTELallowedchipsets)
        self.Vendor_Chq_List.SetCheckedStrings(self.config.vendor)
        self.useLast_Btn.SetValue(False)

    def Select_Last_Run(self, evt):
        print("Loading last run")
# end of class GUI_Window

class MyApp(wx.App):
    def OnInit(self):
        self.GUI_FRAME = GUI_Window(None, wx.ID_ANY, "")
        self.SetTopWindow(self.GUI_FRAME)
        self.GUI_FRAME.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

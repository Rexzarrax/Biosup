#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.1 on Thu Feb 21 22:41:09 2019
#

import wx
import os

from time import sleep

from loadConfig import loadConfig 

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class BIOSUP_CONFIG(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: BIOSUP_CONFIG.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.selectall = self.running = True
        self.allchiparr = []

        self.STATUS_TEXT_CTRL = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)
        self.STATUS_TEXT_CTRL.AppendText("Loading 'GUI_config.ini'...\n")

        self.config = loadConfig("GUI_config.ini")
       

        self.AMD_SIZER_ALL_CB = wx.CheckBox(self, wx.ID_ANY, "Select All")
        self.AMD_Chq_List = wx.CheckListBox(self, wx.ID_ANY, choices=self.config.AMDallowedchipsets)
        self.INTEL_SIZER_ALL_CB = wx.CheckBox(self, wx.ID_ANY, "Select All")
        self.Intel_Chq_List = wx.CheckListBox(self, wx.ID_ANY, choices=self.config.INTELallowedchipsets)
        self.VENDOR_SIZER_ALL_CB = wx.CheckBox(self, wx.ID_ANY, "Select All")
        self.Vendor_Chq_List = wx.CheckListBox(self, wx.ID_ANY, choices=self.config.vendor)
        self.BROWSER_CB = wx.CheckBox(self, wx.ID_ANY, "FireFox")
        self.CLEANUP_CB = wx.CheckBox(self, wx.ID_ANY, "Remove Zips")
        self.SH_BROWSER_CB = wx.CheckBox(self, wx.ID_ANY, "Show Browser")
        self.useLast_ChqBox = wx.CheckBox(self, wx.ID_ANY, "Last Config")
        self.Selectall_Btn = wx.Button(self, wx.ID_ANY, "SELECT ALL")
        self.Run_Btn = wx.Button(self, wx.ID_ANY, "Generate")

        self.CLEANUP_CB.IsChecked()

        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        #Bind events
        self.Run_Btn.Bind(wx.EVT_BUTTON, self.Run_Event)
        self.Selectall_Btn.Bind(wx.EVT_BUTTON, self.Select_All_Chq_Box)
        self.useLast_ChqBox.Bind(wx.EVT_CHECKBOX, self.Select_Last_Run)
        #self.BROWSER_CB.Bind(wx.EVT_CHECKBOX, )
        #self.CLEANUP_CB.Bind(wx.EVT_CHECKBOX, )
        #self.SH_BROWSER_CB.Bind(wx.EVT_CHECKBOX, )
        self.AMD_SIZER_ALL_CB.Bind(wx.EVT_CHECKBOX, self.singular_Chq_AMD)
        self.INTEL_SIZER_ALL_CB.Bind(wx.EVT_CHECKBOX, self.singular_Chq_INTEL)
        self.VENDOR_SIZER_ALL_CB.Bind(wx.EVT_CHECKBOX, self.singular_Chq_Vendor)
        #self.useLast_ChqBox.SetValue(True)
    
    def singular_Chq_AMD(self, evt):
        if self.AMD_SIZER_ALL_CB.IsChecked():
            self.AMD_Chq_List.SetCheckedStrings(self.config.AMDallowedchipsets)
        else:
            self.deselect_Check_Lists(self.AMD_Chq_List)
    def singular_Chq_INTEL(self, evt):
        if self.INTEL_SIZER_ALL_CB.IsChecked():
            self.Intel_Chq_List.SetCheckedStrings(self.config.INTELallowedchipsets)
        else:
            self.deselect_Check_Lists(self.Intel_Chq_List)
    def singular_Chq_Vendor(self, evt):
        if self.VENDOR_SIZER_ALL_CB.IsChecked():
            self.Vendor_Chq_List.SetCheckedStrings(self.config.vendor)
        else:
            self.deselect_Check_Lists(self.Vendor_Chq_List)

    def Run_Event(self, evt):
            #print("Attempting to run BIOSUP...")
        self.datapath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"\\config.ini"
        if self.Chq_fields():
            #Build the configuration for Biosup core
            with open (self.datapath,"w") as outfile:
                self.STATUS_TEXT_CTRL.AppendText("Writing config file...\n")
                outfile.write("[SETTINGS]\nclean = "+str(self.CLEANUP_CB.IsChecked()))
                self.STATUS_TEXT_CTRL.AppendText("clean = "+str(self.CLEANUP_CB.IsChecked())+"\n")
                outfile.write("\nFireFox = "+str(self.BROWSER_CB.IsChecked()))
                self.STATUS_TEXT_CTRL.AppendText("FireFox = "+str(self.BROWSER_CB.IsChecked())+"\n")
                outfile.write("\nopenBrowser = "+str(self.SH_BROWSER_CB.IsChecked()))
                self.STATUS_TEXT_CTRL.AppendText("openBrowser = "+str(self.SH_BROWSER_CB.IsChecked())+"\n")
                outfile.write("\nsaveState = t")
                outfile.write("\nsleeptimer = 6\nsleepwait = 5")
                outfile.write("\nallowedChipsetsAMD = "+str(",".join(self.AMD_Chq_List.GetCheckedStrings())))
                self.STATUS_TEXT_CTRL.AppendText("Allowed AMD chipsets = "+str(",".join(self.AMD_Chq_List.GetCheckedStrings()))+"\n")
                outfile.write("\nallowedChipsetsIntel = "+str(",".join(self.Intel_Chq_List.GetCheckedStrings())))
                self.STATUS_TEXT_CTRL.AppendText("Allowed INTEL chipsets = "+str(",".join(self.Intel_Chq_List.GetCheckedStrings()))+"\n")
                outfile.write("\nallowedChipsets = "+str(",".join(self.allchiparr)))
                outfile.write("\nallowedChipsetsAddon = [CIM]?")
                outfile.write("\nvendor = "+str(",".join(self.Vendor_Chq_List.GetCheckedStrings())))
                self.STATUS_TEXT_CTRL.AppendText("Allowed Vendors = "+str(",".join(self.Vendor_Chq_List.GetCheckedStrings()))+"\n")
                #self.STATUS_TEXT_CTRL.AppendText("Done...\n")
            self.STATUS_TEXT_CTRL.AppendText("Creating Config...\n")
            #self.Create_Thread()
        elif self.useLast_ChqBox.IsChecked():
            self.STATUS_TEXT_CTRL.AppendText("Overwriting old config...\n")
            #self.Create_Thread()
        else:
            self.STATUS_TEXT_CTRL.AppendText("Select at least 1 chipset and vendor or tick 'Run last config' \n")

    #def Create_Thread(self):
    #    try:
    #        self.biosCore = threading.Thread(None, BIOSUP.main())
    #        self.biosCore.start()
    #    except:
    #        self.STATUS_TEXT_CTRL.AppendText("Unable to start thread...\n")

    def Chq_fields(self):
        self.allchiparr = self.AMD_Chq_List.GetCheckedStrings() + self.Intel_Chq_List.GetCheckedStrings()
        self.allarr = self.allchiparr + self.Vendor_Chq_List.GetCheckedStrings()
        
        if not len(self.allarr) == 0:    
            return True
        else:
            return False

    def Select_All_Chq_Box(self, evt): 
        if self.selectall:
            self.STATUS_TEXT_CTRL.AppendText("Selected all tick boxes\n")
            self.Set_Check_Lists(self.config)
            self.useLast_ChqBox.SetValue(False)
            self.selectall = False
            self.Selectall_Btn.SetLabel("De-select All")
        else:
            self.STATUS_TEXT_CTRL.AppendText("Unselecting all tick boxes\n")
            self.useLast_ChqBox.SetValue(False)
            self.deselect_Check_Lists(self.AMD_Chq_List)
            self.deselect_Check_Lists(self.Intel_Chq_List)
            self.deselect_Check_Lists(self.Vendor_Chq_List)
            self.selectall = True
            self.Selectall_Btn.SetLabel("Select All")

    def deselect_Check_Lists(self, mylist):
        for cb in mylist.GetCheckedItems():
                mylist.Check(cb, False)

    def Set_Check_Lists(self, config):
        self.AMD_Chq_List.SetCheckedStrings(config.AMDallowedchipsets)
        self.Intel_Chq_List.SetCheckedStrings(config.INTELallowedchipsets)
        self.Vendor_Chq_List.SetCheckedStrings(config.vendor)

    def Select_Last_Run(self, evt):
        if self.useLast_ChqBox.IsChecked():
            self.STATUS_TEXT_CTRL.AppendText("Loading last run\n")
            self.deselect_Check_Lists(self.AMD_Chq_List)
            self.deselect_Check_Lists(self.Intel_Chq_List)
            self.deselect_Check_Lists(self.Vendor_Chq_List)
            self.lastconfig = loadConfig("config.ini")
            self.Set_Check_Lists(self.lastconfig)
        else:
            self.STATUS_TEXT_CTRL.AppendText("Unchecked 'Last Run'\n")


    def __set_properties(self):
        # begin wxGlade: BIOSUP_CONFIG.__set_properties
        self.SetTitle("BIOSUP")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("C:\\Users\\user\\Desktop\\Dev\\Base Complete\\Project_Biosup\\biosup_noPLEase\\ICO_BIOSUP.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.STATUS_TEXT_CTRL.SetMinSize((175, 250))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: BIOSUP_CONFIG.__do_layout
        ALL_CTRLR = wx.BoxSizer(wx.HORIZONTAL)
        FAT_CONTROLLER_GRID_SIZER = wx.FlexGridSizer(5, 3, 0, 0)
        VENDOR_Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Vendor"), wx.VERTICAL)
        INTEL_Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "INTEL"), wx.VERTICAL)
        AMD_Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "AMD"), wx.VERTICAL)
        ALL_CTRLR.Add(self.STATUS_TEXT_CTRL, 0, wx.EXPAND, 0)
        AMD_Sizer.Add(self.AMD_SIZER_ALL_CB, 0, 0, 0)
        AMD_Sizer.Add(self.AMD_Chq_List, 0, 0, 0)
        FAT_CONTROLLER_GRID_SIZER.Add(AMD_Sizer, 1, wx.EXPAND, 0)
        INTEL_Sizer.Add(self.INTEL_SIZER_ALL_CB, 0, 0, 0)
        INTEL_Sizer.Add(self.Intel_Chq_List, 0, 0, 0)
        FAT_CONTROLLER_GRID_SIZER.Add(INTEL_Sizer, 1, wx.EXPAND, 0)
        VENDOR_Sizer.Add(self.VENDOR_SIZER_ALL_CB, 0, 0, 0)
        VENDOR_Sizer.Add(self.Vendor_Chq_List, 0, 0, 0)
        FAT_CONTROLLER_GRID_SIZER.Add(VENDOR_Sizer, 1, wx.EXPAND, 0)
        FAT_CONTROLLER_GRID_SIZER.Add(self.BROWSER_CB, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        FAT_CONTROLLER_GRID_SIZER.Add(self.CLEANUP_CB, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        FAT_CONTROLLER_GRID_SIZER.Add(self.SH_BROWSER_CB, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        FAT_CONTROLLER_GRID_SIZER.Add(self.useLast_ChqBox, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        FAT_CONTROLLER_GRID_SIZER.Add((0, 0), 0, 0, 0)
        FAT_CONTROLLER_GRID_SIZER.Add((0, 0), 0, 0, 0)
        FAT_CONTROLLER_GRID_SIZER.Add((0, 0), 0, 0, 0)
        FAT_CONTROLLER_GRID_SIZER.Add((0, 0), 0, 0, 0)
        FAT_CONTROLLER_GRID_SIZER.Add((0, 0), 0, 0, 0)
        FAT_CONTROLLER_GRID_SIZER.Add((0, 0), 0, 0, 0)
        FAT_CONTROLLER_GRID_SIZER.Add(self.Selectall_Btn, 0, wx.ALIGN_CENTER, 0)
        FAT_CONTROLLER_GRID_SIZER.Add(self.Run_Btn, 0, wx.ALIGN_RIGHT, 0)
        ALL_CTRLR.Add(FAT_CONTROLLER_GRID_SIZER, 0, 0, 0)
        self.SetSizer(ALL_CTRLR)
        ALL_CTRLR.Fit(self)
        self.Layout()
        # end wxGlade


# end of class BIOSUP_CONFIG

class MyApp(wx.App):
    def OnInit(self):
        self.BIO_FRAME = BIOSUP_CONFIG(None, wx.ID_ANY, "")
        self.SetTopWindow(self.BIO_FRAME)
        self.BIO_FRAME.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    BIOSUP = MyApp(0)
    BIOSUP.MainLoop()

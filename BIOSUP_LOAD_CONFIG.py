from configparser import ConfigParser
import os
from json import load

class loadConfig:
    def __init__(self, configfile, obj_print):
        try:
            config_object = ConfigParser()
            config_object.read(configfile)

            self.allvendordata = {}
            #config
            self.clean = self.str_to_bool((config_object["SETTINGS"]["clean"])) 
            #self.FireFox = self.str_to_bool((config_object["SETTINGS"]["FireFox"])) 
            self.openBrowser = self.str_to_bool((config_object["SETTINGS"]["openBrowser"]))
            self.sleepTimer = int(config_object["SETTINGS"]["sleeptimer"])
            self.sleepwait = int(config_object["SETTINGS"]["sleepwait"])
            self.vendor = (config_object["SETTINGS"]["vendor"]).split(",")
            self.allowedExtras = (config_object["SETTINGS"]["allowedChipsetsAddon"])
            self.saveState = (config_object["SETTINGS"]["saveState"])
            #Builds the 'allowedchipsets' array to sort incoming models in setup.py
            try:
                self.AMDallowedchipsets = config_object["SETTINGS"]["allowedChipsetsAMD"].split(",")
                self.INTELallowedchipsets = config_object["SETTINGS"]["allowedChipsetsIntel"].split(",")
                self.allowedChipsets = (self.AMDallowedchipsets+self.INTELallowedchipsets)
            except:
                self.allowedChipsets = (config_object["SETTINGS"]["allowedChipsets"].split(","))
                print('allowed chipsets')
            self.allowedChipsets.sort()
            #Build a json object to hold all relevent vendor information, either from config file or from vendorinfo.txt
            #try:
                #to be deprecated
                #self.vendorSort = (config_object["SETTINGS"]["vendorSort"].split(","))
                #self.vendorDownloadURLbase = (config_object["SETTINGS"]["vendorDownloadURLbase"].split(","))
                #self.vendorURLaddon = (config_object["SETTINGS"]["vendorURLaddon"].split(","))
                #for x in range (len(self.vendor)):
                #    self.allvendordata[self.vendor[x]] = {"vendorSort":self.vendorSort[x],
                #                    "vendorDownloadURLbase":self.vendorDownloadURLbase[x],
                #                    "vendorURLaddon":self.vendorURLaddon[x]}  
            #except Exception as e: 
            #    print("Failure in Loading vendor data from config "+str(e))
            try:
                self.datapath = os.path.join(os.getcwd(), os.path.dirname(__file__),"vendorInfo.txt")
                with open (self.datapath) as infile:
                    self.allvendordata = load(infile)
                    infile.close()
            except Exception as e: 
                obj_print.print_msg("Failure in loading vendors (in)"+str(e))
                exit()
            obj_print.print_msg(str(self.allvendordata))
        except Exception as e: 
            obj_print.print_msg("Failure in loading vendors (out)"+str(e))
            input("Critical Error: Missing or Invalid configuration file(config.ini or GUI_config.ini)")
            exit()
        #print all loaded config data to console
        obj_print.print_msg("Loading config... ")
        obj_print.print_msg(" >Clean up: "+str(self.clean))
        #print(" >FireFox installed: "+str(self.FireFox))
        obj_print.print_msg(" >Open browser window: "+str(self.openBrowser))
        obj_print.print_msg(" >Save BIOS already Downloaded: "+str(self.saveState))
        obj_print.print_msg(" >Sleep Timer: "+ str(self.sleepTimer))
        obj_print.print_msg(" >Sleep Wait: "+ str(self.sleepwait))
        obj_print.print_msg(" >Vendor Array: "+str(self.vendor))
        obj_print.print_msg(" >Allowed Chipsets: "+str(self.allowedChipsets))
        obj_print.print_msg(" >Allowed Extras: "+str(self.allowedExtras))
        try:
            obj_print.print_msg(" >Vendor Web Selector: "+str(self.vendorSort))
            obj_print.print_msg(" >Additions for URL:"+str(self.vendorURLaddon))
            obj_print.print_msg(" >Download URL base: "+str(self.vendorDownloadURLbase))
        except:
            obj_print.print_msg(str(self.allvendordata))
        obj_print.print_msg("Configuration Loaded...")
    def str_to_bool(self, s):
        if len(s)>0:
            return True
        elif len(s) == 0:
            return False
        else:
            raise ValueError
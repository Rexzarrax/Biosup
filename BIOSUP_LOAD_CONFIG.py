from configparser import ConfigParser
import os
from json import load

class loadConfig:
    def __init__(self, configfile, str_datapath):
        self.str_datapath = str_datapath
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
            try:
                self.allowedChipsets.remove('')
            except:
                print("No blank entries :)")
            try:
                with open (self.str_datapath) as infile:
                    self.allvendordata = load(infile)
                    infile.close()
            except Exception as e: 
                input("Failure in loading vendors (in)"+str(e))
                quit()
            print(str(self.allvendordata))
        except Exception as e: 
            print("Failure in loading vendors (out)"+str(e))
            input("Critical Error: Missing or Invalid configuration file: "+configfile)
            quit()
        #print all loaded config data to console
        print("Loading config... ")
        print(" >Clean up: "+str(self.clean))
        #print(" >FireFox installed: "+str(self.FireFox))
        print(" >Open browser window: "+str(self.openBrowser))
        print(" >Save BIOS already Downloaded: "+str(self.saveState))
        print(" >Sleep Timer: "+ str(self.sleepTimer))
        print(" >Sleep Wait: "+ str(self.sleepwait))
        print(" >Vendor Array: "+str(self.vendor))
        print(" >Allowed Chipsets: "+str(self.allowedChipsets))
        print(" >Allowed Extras: "+str(self.allowedExtras))
        try:
            print(" >Vendor Web Selector: "+str(self.vendorSort))
            print(" >Additions for URL:"+str(self.vendorURLaddon))
            print(" >Download URL base: "+str(self.vendorDownloadURLbase))
        except:
            print(str(self.allvendordata))
        print("Configuration Loaded...")
    def str_to_bool(self, s):
        if len(s)>0:
            return True
        elif len(s) == 0:
            return False
        else:
            raise ValueError
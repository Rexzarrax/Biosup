from configparser import ConfigParser
import os

class loadConfig:
    def __init__(self, configfile):
        try:
            config_object = ConfigParser()
            config_object.read(configfile)

            self.allvendordata = {}

            #config
            self.clean = bool(config_object["SETTINGS"]["clean"]) 
            self.FireFox = bool(config_object["SETTINGS"]["FireFox"]) 
            self.openBrowser = bool(config_object["SETTINGS"]["openBrowser"])
            self.sleepTimer = int(config_object["SETTINGS"]["sleeptimer"])
            self.sleepwait = int(config_object["SETTINGS"]["sleepwait"])
            self.vendor = (config_object["SETTINGS"]["vendor"]).split(",")
            self.vendorSort = (config_object["SETTINGS"]["vendorSort"].split(","))
            try:
                self.AMDallowedchipsets = (config_object["SETTINGS"]["allowedChipsetsAMD"].split(","))
                self.AMDallowedchipsets.sort()
                self.INTELallowedchipsets = (config_object["SETTINGS"]["allowedChipsetsIntel"].split(","))
                self.INTELallowedchipsets.sort()
                self.allowedChipsets = (self.AMDallowedchipsets+self.INTELallowedchipsets)
            except:
                self.allowedChipsets = (config_object["SETTINGS"]["allowedChipsets"].split(","))
            self.allowedChipsets.sort()
            
            try:
                self.allowedExtras = (config_object["SETTINGS"]["allowedChipsetsAddon"])
                self.vendorDownloadURLbase = (config_object["SETTINGS"]["vendorDownloadURLbase"].split(","))
                self.vendorURLaddon = (config_object["SETTINGS"]["vendorURLaddon"].split(","))
                self.saveState = (config_object["SETTINGS"]["saveState"])
                for x in range (len(self.vendor)):
                    self.allvendordata[self.vendor[x]] = {'vendorSort':self.vendorSort[x],
                                    'vendorDownloadURLbase':self.vendorDownloadURLbase[x],
                                    'vendorURLaddon':self.vendorURLaddon[x]}  
            except:
                try:
                    self.datapath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"\\vendorInfo.txt"
                    with open (self.datapath,"w") as infile:
                        self.allvendordata = infile.readlines()
                except:
                    print("Error loading config")
                    exit()


            print(str(self.allvendordata))
        except:
            input("Error: Missing or Invalid configuration file(config.ini)")
            exit()

        print("Loading config... ")
        print(" >Clean up: "+str(self.clean))
        print(" >FireFox installed: "+str(self.FireFox))
        print(" >Open browser window: "+str(self.openBrowser))
        print(" >Save BIOS already Downloaded: "+str(self.saveState))
        print(" >Sleep Timer: "+ str(self.sleepTimer))
        print(" >Sleep Wait: "+ str(self.sleepwait))
        print(" >Vendor Array: "+str(self.vendor))
        print(" >Vendor Web Selector: "+str(self.vendorSort))
        print(" >Allowed Chipsets: "+str(self.allowedChipsets))
        print(" >Allowed Extras: "+str(self.allowedExtras))
        print(" >Download URL base: "+str(self.vendorDownloadURLbase))
        print(" >Additions for URL:"+str(self.vendorURLaddon))
        print("Configuration Loaded...")
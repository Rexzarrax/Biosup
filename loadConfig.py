from configparser import ConfigParser
import os
from json import load

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
            self.allowedExtras = (config_object["SETTINGS"]["allowedChipsetsAddon"])
            self.saveState = (config_object["SETTINGS"]["saveState"])
            #Builds the 'allowedcjipsets' array to sort incoming models in setup.py
            try:
                self.AMDallowedchipsets = (config_object["SETTINGS"]["allowedChipsetsAMD"].split(","))
                self.INTELallowedchipsets = (config_object["SETTINGS"]["allowedChipsetsIntel"].split(","))
                self.allowedChipsets = (self.AMDallowedchipsets+self.INTELallowedchipsets)
            except:
                self.allowedChipsets = (config_object["SETTINGS"]["allowedChipsets"].split(","))
            self.allowedChipsets.sort()
            #Build a json object to hold all relevent vendor information, either from config file or from vendorinfo.txt
            try:
                #to be deprecated
                self.vendorSort = (config_object["SETTINGS"]["vendorSort"].split(","))
                self.vendorDownloadURLbase = (config_object["SETTINGS"]["vendorDownloadURLbase"].split(","))
                self.vendorURLaddon = (config_object["SETTINGS"]["vendorURLaddon"].split(","))
                for x in range (len(self.vendor)):
                    self.allvendordata[self.vendor[x]] = {"vendorSort":self.vendorSort[x],
                                    "vendorDownloadURLbase":self.vendorDownloadURLbase[x],
                                    "vendorURLaddon":self.vendorURLaddon[x]}  
            except Exception as e: 
                print("Failure in Loading vendor data from config "+str(e))
                try:
                    self.datapath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"\\vendorInfo.txt"
                    with open (self.datapath) as infile:
                        self.allvendordata = load(infile)
                        infile.close()
                except Exception as e: 
                    print("Failure in loading vendors "+str(e))
                    exit()
            print(str(self.allvendordata))
        except Exception as e: 
            print("Failure in loading vendors "+str(e))
            input("Error: Missing or Invalid configuration file(config.ini)")
            exit()
        #print all loaded config data to console
        print("Loading config... ")
        print(" >Clean up: "+str(self.clean))
        print(" >FireFox installed: "+str(self.FireFox))
        print(" >Open browser window: "+str(self.openBrowser))
        print(" >Save BIOS already Downloaded: "+str(self.saveState))
        print(" >Sleep Timer: "+ str(self.sleepTimer))
        print(" >Sleep Wait: "+ str(self.sleepwait))
        print(" >Vendor Array: "+str(self.vendor))
        try:
            print(" >Vendor Web Selector: "+str(self.vendorSort))
            print(" >Additions for URL:"+str(self.vendorURLaddon))
            print(" >Download URL base: "+str(self.vendorDownloadURLbase))
        except:
            print(str(self.allvendordata))
        print(" >Allowed Chipsets: "+str(self.allowedChipsets))
        print(" >Allowed Extras: "+str(self.allowedExtras))
        print("Configuration Loaded...")
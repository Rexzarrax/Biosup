import sys
import requests
import os
import time

from Unzip import unzip
from getHTML import gethtml
from biosDL import biosDownload
from setup import setUp
from statistics import datastatistics
from configparser import ConfigParser
from getwebwithjs import webwithjs
from linkSearching import searchForLink

#stores motherboard data
class moboData:
    def __init__(self, mysetup, myGetWeb, vendor, allowedChipsets, allowedExtras):
        #need to make variable, based on length of vendor array in main
        self.allVenArr = []
        for x in range(len(vendor)):
            self.allVenArr.append([])
        mysetup.dl_Src_PCPP(vendor, self.allVenArr, allowedChipsets, allowedExtras)
           

class loadConfig:
    def __init__(self):
        try:
            config_object = ConfigParser()
            config_object.read("config.ini")

            #config
            self.clean = bool(config_object["SETTINGS"]["clean"]) 
            self.FireFox = bool(config_object["SETTINGS"]["FireFox"]) 
            self.openBrowser = bool(config_object["SETTINGS"]["openBrowser"])
            self.sleepTimer = int(config_object["SETTINGS"]["sleeptimer"])
            self.vendor = (config_object["SETTINGS"]["vendor"]).split(",")
            self.vendorSort = (config_object["SETTINGS"]["vendorSort"].split(","))
            self.allowedChipsets = (config_object["SETTINGS"]["allowedChipsetsAMD"].split(","))+(config_object["SETTINGS"]["allowedChipsetsIntel"].split(","))
            self.allowedExtras = (config_object["SETTINGS"]["allowedChipsetsAddon"])
        except:
            input("Error: Missing or Invalid configuration file(config.ini)")
            exit()

        print("Loading config... ")
        print("Clean up: "+str(self.clean))
        print("FireFox installed: "+str(self.FireFox))
        print("Open browser window: "+str(self.openBrowser))
        print("Sleep Timer: "+ str(self.sleepTimer))
        print("Vendor Array: "+str(self.vendor))
        print("Vendor Web Selector: "+str(self.vendorSort))
        print("Allowed Chipsets: "+str(self.allowedChipsets))
        print("Allowed Extras: "+str(self.allowedExtras))

def main():
    print("----------BIOSUP----------")
    print("Initialising...")
    statisticsData = datastatistics()

    modelCount = 0
    modelTotal = 0
    breaker = "-------------------START---------------------"

    myConfig = loadConfig()
    mysetup = setUp()
    myGetWeb = gethtml()
    myData = moboData(mysetup, myGetWeb, myConfig.vendor, myConfig.allowedChipsets, myConfig.allowedExtras)  
    getBIO = biosDownload()
    dezip = unzip()
    print("Opening browser...")
    driver = webwithjs(myConfig.FireFox, myConfig.openBrowser, myConfig.sleepTimer)
    linkSearching = searchForLink()  
    print("Sourcing models...")
    for ven2 in range(len(myConfig.vendor)):
        mysetup.folderChq(myConfig.vendor[ven2])
        myData.allVenArr[ven2].sort()
        mysetup.arrClean(myData.allVenArr[ven2])
        print("\n"+str(myData.allVenArr[ven2])+"\n")
    
    for modelArr in range (len (myConfig.vendor)):
        for modelStr in myData.allVenArr[modelArr]:
            print(breaker)   
            cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/"+myConfig.vendor[modelArr]+"/"+str(modelStr).replace("/","-")+".zip"
            print(modelStr+"|Progress: "+str(myData.allVenArr[modelArr].index(modelStr)+1)+"/"+str(len(myData.allVenArr[modelArr])))
            if myConfig.vendor[modelArr] == "ASUS":
                getBIO.urlBuilderAsus(modelStr ,myConfig.vendorSort[modelArr], cpath, driver, linkSearching)
            elif myConfig.vendor[modelArr] == "ASROCK":
                getBIO.urlBuilderAsrock(modelStr,myConfig.vendorSort[modelArr], cpath, driver, linkSearching)
            elif myConfig.vendor[modelArr] == "MSI":
                getBIO.urlBuilderMSI(modelStr ,myConfig.vendorSort[modelArr], cpath, driver, linkSearching)
            elif myConfig.vendor[modelArr] == "GIGABYTE":
                getBIO.urlBuilderGigabyte(modelStr ,myConfig.vendorSort[modelArr], cpath, driver, linkSearching)
            dezip.deZip(cpath, cpath.strip(".zip"))
            print("All actions Attempted, moving to next BIOS...\n")

        statisticsData.statistics(myData, myConfig.vendor[modelArr], modelArr)
        if myConfig.clean:
            print("Running Cleanup of "+myConfig.vendor[modelArr]+"...")
            mysetup.cleanup(myData.allVenArr[modelArr], myConfig.vendor[modelArr])

    driver.driver.quit()
    print("All downloading and unzipping attempted...\n")
    
    statisticsData.printstat(myConfig.vendor)
    
    print("Script Finished...")
    input("Press Enter to continue/exit...")

if __name__ == "__main__":
    main()


#extra scopes:
#-> generate local lists to reduce dl time in future
#-> cli/gui menu system
#-> options for specific sources/vendors
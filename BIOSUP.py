import sys
import requests
import os
import time
import json

from csv import writer
from Unzip import unzip
from getHTML import gethtml
from biosDL import biosDownload
from setup import setUp
from statistics import datastatistics
from configparser import ConfigParser
from getwebwithjs import webwithjs
from linkSearching import searchForLink          

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
            self.sleepwait = int(config_object["SETTINGS"]["sleepwait"])
            self.vendor = (config_object["SETTINGS"]["vendor"]).split(",")
            self.vendorSort = (config_object["SETTINGS"]["vendorSort"].split(","))
            self.allowedChipsets = (config_object["SETTINGS"]["allowedChipsetsAMD"].split(","))+(config_object["SETTINGS"]["allowedChipsetsIntel"].split(","))
            self.allowedExtras = (config_object["SETTINGS"]["allowedChipsetsAddon"])
            self.vendorDownloadURLbase = (config_object["SETTINGS"]["vendorDownloadURLbase"].split(","))
            self.vendorURLaddon = (config_object["SETTINGS"]["vendorURLaddon"].split(","))
            self.saveState = (config_object["SETTINGS"]["saveState"])
        except:
            input("Error: Missing or Invalid configuration file(config.ini)")
            exit()

        print("Loading config... ")
        print(" > Clean up: "+str(self.clean))
        print(" > FireFox installed: "+str(self.FireFox))
        print(" > Open browser window: "+str(self.openBrowser))
        print(" > Save BIOS already Downloaded: "+str(self.saveState))
        print(" > Sleep Timer: "+ str(self.sleepTimer))
        print(" > Sleep Timer: "+ str(self.sleepwait))
        print(" > Vendor Array: "+str(self.vendor))
        print(" > Vendor Web Selector: "+str(self.vendorSort))
        print(" > Allowed Chipsets: "+str(self.allowedChipsets))
        print(" > Allowed Extras: "+str(self.allowedExtras))
        print(" > Download URL base: "+str(self.vendorDownloadURLbase))
        print(" > Additions for URL:"+str(self.vendorURLaddon))
        print("Configuration Loaded...")

#stores motherboard data
class moboData:
    def __init__(self, mysetup, myGetWeb, vendor, allowedChipsets, allowedExtras):
        #need to make variable, based on length of vendor array in main
        self.allVenArr = []
        for x in range(len(vendor)):
            self.allVenArr.append([])
        mysetup.dl_Src_PCPP(vendor, self.allVenArr, allowedChipsets, allowedExtras)

def main():
    print("----------BIOSUP----------")
    print("Initialising...")
    #modelData = []
    modelData = {}
    modelData['model'] = []
    #status status'-> 0=nothing attempted, 1= BIOS successfully downloaded, 2=Bios failed to downloaded, 4= already downloaded and upto date
    #modelData['model'].append({'name':'','productURL':'','downloadURL':'','status':0,'vendor':'',chipset':''})

    modelCount = 0
    modelTotal = 0
    datapath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"\\BIOSHERE\\urlData.txt"
    breaker = "-------------------START---------------------"

    #set up directories and files
    try: 
        with open(datapath) as datafile:
            #modelData = datafile.read().split("\n")
            modelData = json.load(datafile)
            datafile.close()
    except:
        try:
            print("Attempting to create BIOSHERE folder...")
            os.mkdir(os.path.join(os.getcwd(), os.path.dirname(__file__))+"\\BIOSHERE\\")
        except:
            print("Dir already exists")
        try:
            print("Creating "+datapath)
            datafile=open(datapath,"x")
            datafile.close()
        except:
            print('File already exists...')

    print(str(modelData))
    #create required objects
    myConfig = loadConfig()
    statisticsData = datastatistics(myConfig.vendor)
    mysetup = setUp()
    myGetWeb = gethtml()
    myData = moboData(mysetup, myGetWeb, myConfig.vendor, myConfig.allowedChipsets, myConfig.allowedExtras)  
    getBIO = biosDownload()
    dezip = unzip()

    #open headless web browser to access vendor websites
    print("Opening browser...")
    driver = webwithjs(myConfig.FireFox, myConfig.openBrowser, myConfig.sleepTimer)
    linkSearching = searchForLink()

    print("Sourcing models...")
    for vendorName in range(len(myConfig.vendor)):
        mysetup.folderChq(myConfig.vendor[vendorName])
        myData.allVenArr[vendorName].sort()
        mysetup.arrClean(myData.allVenArr[vendorName])
        print("\n"+str(myData.allVenArr[vendorName])+"\n")
    
    print("Finding and Downloading BIOS...")
    for modelArr in range (len (myConfig.vendor)):
        for modelStr in myData.allVenArr[modelArr]:
            timeMod = time.time()
            success = False
            print(breaker)   
            cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/BIOSHERE/"+myConfig.vendor[modelArr]+"/"+str(modelStr).replace("/","-")+".zip"
            print(modelStr+"|Progress: "+str(myData.allVenArr[modelArr].index(modelStr)+1)+"/"+str(len(myData.allVenArr[modelArr])))
            if myConfig.vendor[modelArr] == "ASUS":
                getBIO.urlBuilderAsus(modelStr,myConfig.vendorSort[modelArr], 
                                        cpath, driver, 
                                        myConfig.vendorDownloadURLbase[modelArr], modelData, 
                                        linkSearching)
            else:
                getBIO.GenericUrlBuilder(modelStr,myConfig.vendorSort[modelArr], 
                                        cpath, driver, 
                                        myConfig.vendorDownloadURLbase[modelArr],myConfig.vendorURLaddon[modelArr], 
                                        modelData, linkSearching)

            dezip.deZip(cpath, cpath.strip(".zip"))
            statisticsData.statistics(myData, myConfig.vendor[modelArr], modelArr, modelStr, getBIO.status)
            if (time.time() - timeMod)<myConfig.sleepTimer:
                print("Sleeping...")
                time.sleep(myConfig.sleepwait) 
            print("Moving to next BIOS...\n")
        if myConfig.clean:
                print("Running Cleanup of "+myConfig.vendor[modelArr]+"...")
                mysetup.cleanup(myData.allVenArr[modelArr], myConfig.vendor[modelArr])
        print("Adding URL's to file...")
        if myConfig.saveState:
            with open (datapath,"w") as outfile:
                json.dump(modelData,outfile)

    driver.driver.quit()
    print("All downloading and unzipping attempted...\n")

    statisticsData.printstat(myConfig.vendor, myData)
    
    print("Script Finished...")
    input("Press Enter to continue/exit...")

if __name__ == "__main__":
    main()


#extra scopes:
#-> generate local lists to reduce dl time in future
#-> cli/gui menu system
#-> options for specific sources/vendors
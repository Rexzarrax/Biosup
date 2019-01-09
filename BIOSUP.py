import sys
import requests
import os
import time

from Unzip import unzip
from getHTML import gethtml
from biosDL import bioufiDL
from setup import setUp
from statistics import datastatistics
from configparser import ConfigParser
from getwebwithjs import webwithjs

#stores motherboard data
class moboData:
    def __init__(self, mysetup, myGetWeb, vendor, PLESrc):
        #need to make variable, based on length of vendor array in main
        self.asrockArr = []
        self.asusArr = []
        self.gigabyteArr = []
        self.msiArr = []

        self.allVenArr = [self.asrockArr, self.asusArr, self.gigabyteArr, self.msiArr]
        if PLESrc == True:
            print("Src = PLE")
            for ven in range(len(vendor)):
                mysetup.dl_Src_PLE_API(vendor[ven], self.allVenArr[ven])
                #mysetup.dl_Src_PLE(myGetWeb, vendor[ven], self.allVenArr[ven])
        else:
            print("Src = PCPP")
            #for ven in range(len(self.allVenArr)):
            mysetup.dl_Src_PCPP(vendor, self.allVenArr)
           
#initial checks and basic file creation
def main():
    print("----------BIOSUP----------")
    print("Initialising...")
    statisticsData = datastatistics()

    modelCount = 0
    modelTotal = 0
    breaker = "-------------------START---------------------"
    try:
        config_object = ConfigParser()
        config_object.read("config.ini")

        #config
        clean = bool(config_object["SETTINGS"]["clean"]) #delete zip files once done
        FireFox = bool(config_object["SETTINGS"]["FireFox"]) #need to find way to reduce amount of passthrough
        openBrowser = bool(config_object["SETTINGS"]["openBrowser"])#to see where the browser is going to
        PLESrc = bool(config_object["SETTINGS"]["PLESrc"]) #Get model from PLE 
        sleepTimer = int(config_object["SETTINGS"]["sleeptimer"])
        #vendor = ["ASROCK","ASUS", "GIGABYTE", "MSI"]
        #vendor = ["ASUS"]
        vendor = (config_object["SETTINGS"]["vendor"]).split(",")
    except:
        input("Missing/invalid configuration file")

    print("Loading config... ")
    print("Clean up: "+str(clean))
    print("FireFox installed: "+str(FireFox))
    print("Open browser window: "+str(openBrowser))
    print("Use PLE Website for models: "+str(PLESrc))
    print("Sleep Timer: "+ str(sleepTimer))
    print("Vendor Array: "+str(vendor))

    mysetup = setUp()
    myGetWeb = gethtml()
    myData = moboData(mysetup, myGetWeb, vendor, PLESrc)  
    getBIO = bioufiDL()
    dezip = unzip()
    print("Opening browser...")
    browser = webwithjs(FireFox, openBrowser, sleepTimer)

    print(vendor)     
    
    print("Sourcing models...")
    #Sort the arrays ready for further processing+delete duplicate entries
    for ven2 in range(len(vendor)):
        mysetup.folderChq(vendor[ven2])
        myData.allVenArr[ven2].sort()
        mysetup.arrClean(myData.allVenArr[ven2])
        print("\n"+str(myData.allVenArr[ven2])+"\n")
    
    for modelArr in range (len (vendor)):
        for modelStr in myData.allVenArr[modelArr]:
            print(breaker)   
            cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/"+vendor[modelArr]+"/"+str(modelStr).replace("/","-")+".zip"
            print(modelStr+"|Progress: "+str(myData.allVenArr[modelArr].index(modelStr)+1)+"/"+str(len(myData.allVenArr[modelArr])))  
            if vendor[modelArr] == "ASUS":
                getBIO.urlBuilderAsus(modelStr ,"^https:\/\/www\.asus\.com\/", cpath, browser)
            elif vendor[modelArr] == "ASROCK":
                getBIO.urlBuilderAsrock(modelStr,"^https:\/\/www\.asrock\.com\/mb", cpath, browser)
            elif vendor[modelArr] == "MSI":
                getBIO.urlBuilderMSI(modelStr ,"^https:\/\/www\.msi\.com\/Motherboard\/(support\/)?", cpath, browser)
            elif vendor[modelArr] == "GIGABYTE":
                getBIO.urlBuilderGigabyte(modelStr ,"^https:\/\/www\.gigabyte\.com\/(us\/)?Motherboard\/", cpath, browser)
            print("Unzipping: "+cpath)
            dezip.deZip(cpath, cpath.strip(".zip"))
            print("All actions Attempted, moving to next BIOS...\n")

        statisticsData.statistics(myData, vendor[modelArr], modelArr)
        if clean:
            print("Running Cleanup of "+vendor[modelArr]+"...")
            mysetup.cleanup(myData.allVenArr[modelArr], vendor[modelArr])

    browser.driver.quit()
    print("All downloading and unzipping attempted...\n")
    
    statisticsData.printstat(vendor)
    
    print("Script Finished...")
    input("Press Enter to continue/exit...")

if __name__ == "__main__":
    main()


#extra scopes:
#->select src, either PLE or PCPP
#-> generate local lists to reduce dl time in future
#-> cli menu system
#-> options for specific sources/vendors

#planned scopes:
#-> config file

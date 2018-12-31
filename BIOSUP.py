import sys
import requests
import os
import time

from Unzip import unzip
from getHTML import gethtml
from biosDL import bioufiDL
from setup import setUp
from inputFiles import inputfiles
from statistics import statistics
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
        self.miscArr = []

        self.allVenArr = [self.asrockArr, self.asusArr, self.gigabyteArr, self.msiArr]
        if PLESrc == True:
            print("Src = PLE")
            for ven in range(len(self.allVenArr)):
                #mysetup.dl_Src_PLE_API(vendor[ven], self.allVenArr[ven])
                mysetup.dl_Src_PLE(myGetWeb, vendor[ven], self.allVenArr[ven])
        else:
            print("Src = PCPP")
            #for ven in range(len(self.allVenArr)):
            mysetup.dl_Src_PCPP(vendor, self.allVenArr)
           
#initial checks and basic file creation
def main():
    print("----------BIOSUP----------")
    print("Initialising...")

    vendor = ["ASROCK","ASUS", "GIGABYTE", "MSI"]
    modelCount = 0
    modelTotal = 0
    timeStart = time.time()
    breaker = "-------------------START---------------------"

    config_object = ConfigParser()
    config_object.read("config.ini")

    #config
    clean = bool(config_object["SETTINGS"]["clean"]) #delete zip files once done
    FireFox = bool(config_object["SETTINGS"]["FireFox"]) #need to find way to reduce amount of passthrough
    openBrowser = bool(config_object["SETTINGS"]["openBrowser"])#to see where the browser is going to
    PLESrc = bool(config_object["SETTINGS"]["PLESrc"]) #Get model from PLE

    print("Loading config: ")
    print("Clean up: "+str(clean))
    print("FireFox installed: "+str(FireFox))
    print("Use PLE Website for models: "+str(PLESrc))

    mysetup = setUp()
    myGetWeb = gethtml()
    myData = moboData(mysetup, myGetWeb, vendor, PLESrc)  
    getBIO = bioufiDL()
    dezip = unzip()
    print("Opening browser...")
    browser = webwithjs(FireFox, openBrowser)

    print(vendor)

    #create folders
    for ven1 in range(len(vendor)):
        mysetup.folderChq(vendor[ven1])
    
    print("Sourcing models...")
    #Sort the arrays ready for further processing+delete duplicate entries
    for ven2 in range(len(vendor)):
        myData.allVenArr[ven2].sort()
        mysetup.arrClean(myData.allVenArr[ven2])
        print("\n"+str(myData.allVenArr[ven2])+"\n")
    
    for modelArr in range (len (myData.allVenArr)):
        for modelStr in myData.allVenArr[modelArr]:
            print(breaker)   
            cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/"+vendor[modelArr]+"/"+str(modelStr).replace("/","-")+".zip"
            print(modelStr+"'s BIOS...")  
            if vendor[modelArr] == "ASUS":
                getBIO.urlBuilderAsus(myGetWeb, modelStr ,"^https:\/\/www\.asus\.com\/", cpath, browser)
            elif vendor[modelArr] == "ASROCK":
                getBIO.urlBuilderAsrock(myGetWeb, modelStr,"^https:\/\/www\.asrock\.com\/mb", cpath, browser)
            elif vendor[modelArr] == "MSI":
                getBIO.urlBuilderMSI(myGetWeb, modelStr ,"^https:\/\/www\.msi\.com\/Motherboard\/support\/", cpath, browser)
            elif vendor[modelArr] == "GIGABYTE":
                getBIO.urlBuilderGigabyte(myGetWeb, modelStr ,"^https:\/\/www\.gigabyte\.com\/(us\/)?Motherboard\/", cpath, browser)
            print("Unzipping: "+cpath)
            dezip.deZip(cpath, cpath.strip(".zip"))
            print("All actions Attempted, moving to next BIOS...\n")

    print("All download and unzipping attempted...")
    statistics(myData, vendor, timeStart)

    if clean:
        print("Running Cleanup...")
        for v in range(len(vendor)):
            mysetup.cleanup(myData.allVenArr[v], vendor[v])
    browser.driver.quit()
    #print("Statistics are above the deleted files")
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

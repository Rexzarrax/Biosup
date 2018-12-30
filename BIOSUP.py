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
            for ven in range(len(self.allVenArr)):
                mysetup.dl_Src_PCPP(vendor[ven], self.allVenArr[ven])
           
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
    clean = bool(config_object["SETTINGS"]["clean"]) #delete zip file once done
    FireFox = bool(config_object["SETTINGS"]["FireFox"]) #need to find way to reduce amount of passthrough
    PLESrc = bool(config_object["SETTINGS"]["PLESrc"]) #Get model from PLE

    print("Loading config: ")
    print("Clean up: "+str(clean))
    print("FireFox installed: "+str(FireFox))
    print("Use PLE Website for models: "+str(PLESrc))

    mysetup = setUp()
    myGetWeb = gethtml()
    myData = moboData(mysetup, myGetWeb, vendor, PLESrc)  
    myI = inputfiles()
    getBIO = bioufiDL()
    dezip = unzip()

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
    #Get models
    for modelStr in myData.asusArr:
        print(breaker)   
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/ASUS/"+str(modelStr).replace("/","-")+".zip"  
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderAsus(myGetWeb, modelStr ,"^https:\/\/www\.asus\.com\/", cpath, FireFox)
        print("Unzipping: "+cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")
    for modelStr in myData.gigabyteArr:
        print(breaker)
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/GIGABYTE/"+str(modelStr).replace("/","-")+".zip"  
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderGigabyte(myGetWeb, modelStr ,"^https:\/\/www\.gigabyte\.com\/(us\/)?Motherboard\/", cpath, FireFox)
        print("Unzipping: "+cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")
    for modelStr in myData.msiArr:
        print(breaker)   
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/MSI/"+str(modelStr).replace("/","-")+".zip"
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderMSI(myGetWeb, modelStr ,"^https:\/\/www\.msi\.com\/Motherboard\/support\/", cpath, FireFox)
        print("Unzipping: "+cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")
    for modelStr in myData.asrockArr:
        print(breaker) 
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/ASROCK/"+str(modelStr).replace("/","-")+".zip"  
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderAsrock(myGetWeb, modelStr,"^https:\/\/www\.asrock\.com\/mb", cpath, FireFox)
        print("Unzipping: "+cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")

    statistics(myData, vendor, timeStart)

    if clean:
        print("Running Cleanup...")
        for v in range(len(vendor)):
            mysetup.cleanup(myData.allVenArr[v], vendor[v])
    print("Finished...")
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()


#extra scopes:
#->select src, either PLE or PCPP
#-> generate local lists to reduce dl time in future
#-> cli menu system
#-> options for specific sources/vendors

#planned scopes:
#-> config file

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
from getwebwithjs import webwithjs
from linkSearching import searchForLink       
from loadConfig import loadConfig   

#stores motherboard data
class moboData:
    def __init__(self, mysetup, myGetWeb, vendor, allowedChipsets, allowedExtras, modelData):
        self.modelData = modelData
        #status status'-> 0=nothing attempted, 1= BIOS successfully downloaded, 2=Bios failed to downloaded, 4= already downloaded and upto date
        mysetup.dl_Src_PCPP(vendor, self.modelData, allowedChipsets, allowedExtras)

def main():
    print("----------BIOSUP----------")
    print("Initialising...")
    modelData = {}
    datapath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"\\BIOSHERE\\urlData.txt"
    breaker = "-------------------START---------------------"
    #set up directories and files
    try: 
        with open(datapath) as datafile:
            modelData = json.load(datafile)
            print(str(modelData))
            datafile.close()
    except Exception as e: 
        print(e)
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

    #create required objects
    myConfig = loadConfig("config.ini")
    statisticsData = datastatistics(myConfig.vendor)
    mysetup = setUp()
    myGetWeb = gethtml()
    myData = moboData(mysetup, myGetWeb, myConfig.vendor, myConfig.allowedChipsets, myConfig.allowedExtras, modelData)  
    getBIO = biosDownload()
    dezip = unzip()

    #open headless web browser to access vendor websites
    print("Opening browser...")
    driver = webwithjs(myConfig.FireFox, myConfig.openBrowser, myConfig.sleepTimer)
    linkSearching = searchForLink()

    print("Sourcing models...")
    for vendorName in range(len(myConfig.vendor)):
        mysetup.folderChq(myConfig.vendor[vendorName])

    print(str(myData.modelData))
    
    print("Finding and Downloading BIOS...")

    modelLen = len(myData.modelData)

    #loops through all entries in the myData.modelData dictionary
    for index,model in enumerate(myData.modelData):
        timeModerator = time.time()
        success = False
        print(breaker)
        cpathDir = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/BIOSHERE/"+myData.modelData[model]['vendor']+"/"+str(myData.modelData[model]['chipset'])
        print(model+"|Progress: "+str(index+1)+"/"+str(modelLen))
        try:
            os.makedirs(cpathDir)
        except:
            print(cpathDir+" Already Exists...")
        cpathZip = cpathDir+"/"+myData.modelData[model]['name'].replace("/","-")+".zip"
        vendor = myData.modelData[model]['vendor']
        if vendor == "ASUS":
            getBIO.urlBuilderAsus(myData.modelData[model],
                                    myConfig.allvendordata[vendor]['vendorSort'], 
                                    cpathZip, driver, 
                                    myConfig.allvendordata[vendor]['vendorDownloadURLbase'],
                                    linkSearching)
        else:
            getBIO.GenericUrlBuilder(myData.modelData[model],
                                    myConfig.allvendordata[vendor]['vendorSort'], 
                                    cpathZip, driver, 
                                    myConfig.allvendordata[vendor]['vendorDownloadURLbase'],
                                    myConfig.allvendordata[vendor]['vendorURLaddon'], 
                                    linkSearching)

        dezip.deZip(cpathZip, cpathZip.strip(".zip"))
        if (time.time() - timeModerator)<myConfig.sleepTimer:
            print("Sleeping...")
            time.sleep(myConfig.sleepwait) 
        print("Moving to next BIOS...\n")
        if myConfig.clean:
            print("Running Cleanup of "+cpathZip+"...")
            mysetup.cleanup(cpathZip, index)
        if (index%10==0):
            print("Adding last "+str(10)+" URL's to file...")
            if myConfig.saveState:
                with open (datapath,"w") as outfile:
                    json.dump(myData.modelData,outfile)

    if myConfig.saveState:
        with open (datapath,"w") as outfile:
            json.dump(myData.modelData,outfile)

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
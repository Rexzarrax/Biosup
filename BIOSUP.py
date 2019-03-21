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
    def __init__(self, mysetup, myGetWeb, vendor, allowedChipsets, allowedExtras, dict_modelData):
        self.dict_modelData = dict_modelData
        #status status'-> 0=nothing attempted, 1= BIOS successfully downloaded, 2=Bios failed to downloaded, 4= already downloaded and upto date
        mysetup.dl_Src_PCPP(vendor, self.dict_modelData, allowedChipsets, allowedExtras)

def main():
    print("----------BIOSUP----------")
    print("Initialising...")
    dict_ModelData = {}
    str_datapath = os.path.join(os.getcwd(), os.path.dirname(__file__),"BIOSHERE","urlData.txt")
    str_breaker = "-------------------START---------------------"
    #set up directories and files
    try: 
        with open(str_datapath) as file_datafile:
            dict_ModelData = json.load(file_datafile)
            print(str(dict_ModelData))
            file_datafile.close()
    except Exception as e: 
        print(e)
        try:
            print("Attempting to create BIOSHERE folder...")
            os.mkdir(os.path.join(os.getcwd(), os.path.dirname(__file__),"BIOSHERE"))
        except:
            print("Dir already exists")
        try:
            print("Creating "+str_datapath)
            file_datafile=open(str_datapath,"x")
            file_datafile.close()
        except:
            print('File already exists...')

    #create required objects
    obj_myConfig = loadConfig("config.ini")
    obj_statisticsData = datastatistics(obj_myConfig.vendor)
    obj_mysetup = setUp()
    obj_myGetWeb = gethtml()
    obj_myData = moboData(obj_mysetup, obj_myGetWeb, obj_myConfig.vendor, obj_myConfig.allowedChipsets, obj_myConfig.allowedExtras, dict_ModelData)  
    obj_getBIO = biosDownload()
    obj_dezip = unzip()
    
    #open headless web browser to access vendor websites
    print("Opening browser...")
    driver = webwithjs(obj_myConfig.openBrowser, obj_myConfig.sleepTimer)
    obj_linkSearching = searchForLink()

    print("Sourcing models...")
    for vendorName in range(len(obj_myConfig.vendor)):
        obj_mysetup.folderChq(obj_myConfig.vendor[vendorName])

    print(str(obj_myData.dict_modelData))
    
    print("Finding and Downloading BIOS...")

    int_modelLen = len(obj_myData.dict_modelData)

    #loops through all entries in the myData.modelData dictionary
    for int_index,str_model in enumerate(obj_myData.dict_modelData):
        try:
            timeModerator = time.time()
            success = False
            print(str_breaker)
            cpathDir = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/BIOSHERE/"+obj_myData.dict_modelData[str_model]['vendor']+"/"+str(obj_myData.dict_modelData[str_model]['chipset'])
            print(str_model+"|Progress: "+str(int_index+1)+"/"+str(int_modelLen))
            try:
                os.makedirs(cpathDir)
            except:
                print(cpathDir+" Already Exists...")
            str_cpathZip = cpathDir+"/"+obj_myData.dict_modelData[str_model]['name'].replace("/","-")+".zip"
            str_vendor = obj_myData.dict_modelData[str_model]['vendor']
            if str_vendor == "ASUS":
                obj_getBIO.urlBuilderAsus(obj_myData.dict_modelData[str_model],
                        obj_myConfig.allvendordata[str_vendor]['vendorSort'], 
                        str_cpathZip, driver, 
                        obj_myConfig.allvendordata[str_vendor]['vendorDownloadURLbase'],
                        obj_linkSearching)
            else:
                obj_getBIO.GenericUrlBuilder(obj_myData.dict_modelData[str_model],
                        obj_myConfig.allvendordata[str_vendor]['vendorSort'], 
                        str_cpathZip, driver, 
                        obj_myConfig.allvendordata[str_vendor]['vendorDownloadURLbase'],
                        obj_myConfig.allvendordata[str_vendor]['vendorURLaddon'], 
                        obj_linkSearching)

            obj_dezip.deZip(str_cpathZip, str_cpathZip.strip(".zip"))
            if (time.time() - timeModerator)<obj_myConfig.sleepTimer:
                print("Sleeping...")
                time.sleep(obj_myConfig.sleepwait) 
            print("Moving to next BIOS...\n")
            if obj_myConfig.clean:
                print("Running Cleanup of "+str_cpathZip+"...")
                obj_mysetup.cleanup(str_cpathZip, int_index)
            if (int_index%10==0):
                print("Adding last "+str(10)+" URL's to file...")
                if obj_myConfig.saveState:
                    with open (str_datapath,"w") as outfile:
                        json.dump(obj_myData.dict_modelData,outfile)
        except:
            print("Error Detected with ..."+str_model)
            wait = input("Press Enter to continue. \nPress any key and then Enter to exit:")
            if len(wait)>0:
                print('Exiting...')
                driver.driver.quit()
                quit()

    if obj_myConfig.saveState:
        with open (str_datapath,"w") as outfile:
            json.dump(obj_myData.dict_modelData,outfile)

    driver.driver.quit()
    print("All downloading and unzipping attempted...\n")

    obj_statisticsData.printstat(obj_myConfig.vendor, obj_myData)
    
    print("Script Finished...")
    input("Press Enter to continue/exit...")

if __name__ == "__main__":
    main()


#extra scopes:
#-> generate local lists to reduce dl time in future
#-> cli/gui menu system
#-> options for specific sources/vendors
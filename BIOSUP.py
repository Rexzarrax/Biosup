import sys
import requests
import os
import time
import json
import logging

from csv import writer

from BIOSUP_UNZIP_ZIP import unzip
from BIOSUP_GET_RAW_HTML import gethtml
from BIOSUP_FIND_URL_AND_DL import biosDownload
from BIOSUP_DICT_SETUP_DEL import setUp
from BIOSUP_GET_STATISTICS import datastatistics
from BIOSUP_LOAD_PG_IN_DRIVER import webwithjs
from BIOSUP_SEARCH_PRODUCT_LINK import searchForLink       
from BIOSUP_LOAD_CONFIG import loadConfig   

#stores motherboard data
class moboData:
    def __init__(self, obj_mysetup, vendor, allowedChipsets, allowedExtras, dict_modelData):
        self.dict_modelData = dict_modelData
        obj_mysetup.dl_Src_PCPP(vendor, self.dict_modelData, allowedChipsets, allowedExtras)

def main():
    print('----------BIOSUP----------')
    print("Initialising...")
    dict_ModelData = {}
    str_datapath = os.path.join(os.getcwd(), os.path.dirname(__file__),"BIOSHERE","urlData.txt")
    str_breaker = "-------------------START---------------------"
    dict_state_key = {'no_action':0,'update_bios':1,'ignore_bios':2,'failed_dl':3,'success_dl':4, 'up-to-date':5}
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
    obj_myData = moboData(obj_mysetup, obj_myConfig.vendor, obj_myConfig.allowedChipsets, obj_myConfig.allowedExtras, dict_ModelData)  
    obj_getBIO = biosDownload()
    obj_dezip = unzip()
    
    #open headless web browser to access vendor websites
    print("Opening browser...")
    browser_driver = webwithjs(obj_myConfig.openBrowser, obj_myConfig.sleepTimer)
    obj_linkSearching = searchForLink()

    print("Sourcing models...")
    for vendorName in range(len(obj_myConfig.vendor)):
        obj_mysetup.folderChq(obj_myConfig.vendor[vendorName])

    print(str(obj_myData.dict_modelData))
    
    print("Finding and Downloading BIOS...")

    int_used_total = 0

    int_modelLen = len(obj_myData.dict_modelData)
    for int_x,str_model in enumerate(obj_myData.dict_modelData):
        if not obj_myData.dict_modelData[str_model]['status'] == dict_state_key['update_bios']:
            obj_myData.dict_modelData[str_model]['status'] = dict_state_key['ignore_bios']
        else:
            int_used_total += 1

    #loops through all entries in the myData.modelData dictionary
    for int_index,str_model in enumerate(obj_myData.dict_modelData):
        try:
            if obj_myData.dict_modelData[str_model]['status'] == dict_state_key['update_bios']:
                int_timeModerator = time.time()
                bool_success = False
                print(str_breaker)
                str_cpathDir = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/BIOSHERE/"+obj_myData.dict_modelData[str_model]['vendor']+"/"+str(obj_myData.dict_modelData[str_model]['chipset'])
                
                print(str_model+"|Progress: "+str(int_index+1)+"/"+str(int_used_total))
                try:
                    os.makedirs(str_cpathDir)
                except:
                    print(str_cpathDir+" Already Exists...")
                str_cpathZip = str_cpathDir+"/"+obj_myData.dict_modelData[str_model]['name'].replace("/","-")+".zip"
                str_vendor = obj_myData.dict_modelData[str_model]['vendor']
                if (obj_myData.dict_modelData[str_model]['status'] == dict_state_key['no_action']) or (obj_myData.dict_modelData[str_model]['status'] == dict_state_key['update_bios']):
                    if str_vendor == "ASUS":
                        obj_getBIO.urlBuilderAsus(
                                obj_myData.dict_modelData[str_model],
                                obj_myConfig.allvendordata[str_vendor]['vendorSort'], 
                                str_cpathZip, 
                                browser_driver, 
                                obj_myConfig.allvendordata[str_vendor]['vendorDownloadURLbase'],
                                obj_linkSearching)
                    else:
                        obj_getBIO.GenericUrlBuilder(
                                obj_myData.dict_modelData[str_model],
                                obj_myConfig.allvendordata[str_vendor]['vendorSort'], 
                                str_cpathZip, 
                                browser_driver, 
                                obj_myConfig.allvendordata[str_vendor]['vendorDownloadURLbase'],
                                obj_myConfig.allvendordata[str_vendor]['vendorURLaddon'], 
                                obj_linkSearching)
                    if not obj_myData.dict_modelData[str_model]['status'] == dict_state_key['up-to-date'] or obj_myData.dict_modelData[str_model]['status'] == dict_state_key['failed_dl']:
                        obj_dezip.deZip(str_cpathZip, str_cpathZip.strip(".zip"))
                    if (time.time() - int_timeModerator)<obj_myConfig.sleepTimer:
                        print("Sleeping...")
                        time.sleep(obj_myConfig.sleepwait)
                else:
                    print("Skipping "+str_model) 
                print("Moving to next BIOS...\n")
                if obj_myConfig.clean and obj_myData.dict_modelData[str_model]['status'] == dict_state_key['success_dl']:
                    print("Running Cleanup of "+str_cpathZip+"...")
                    obj_mysetup.cleanup(str_cpathZip, int_index)
                if (int_index%10==0):
                    print("Adding last "+str(10)+" URL's to file...")
                    if obj_myConfig.saveState:
                        with open (str_datapath,"w") as outfile:
                            json.dump(obj_myData.dict_modelData,outfile)
            else:
                print("Skipped: "+obj_myData.dict_modelData[str_model]['name'])
        except:
            print("Error Detected with ..."+str_model)
            wait = input("Press Enter to continue. \nPress any key and then Enter to exit:")
            if len(wait)>0:
                print('Exiting...')
                browser_driver.driver.quit()
                quit()

    if obj_myConfig.saveState:
        with open (str_datapath,"w") as outfile:
            json.dump(obj_myData.dict_modelData,outfile)

    browser_driver.driver.quit()
    print("All downloading and unzipping attempted...\n")

    print("Total Models in urldata.txt"+str(int_modelLen)) 

    obj_statisticsData.printstat(obj_myConfig.vendor, obj_myData)
    
    print("Script Finished...")
    input("Press Enter to continue/exit...")

if __name__ == "__main__":
    main()
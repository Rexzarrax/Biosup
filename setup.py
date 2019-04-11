import os
import json
import requests
import re
from PCPartPicker_API import pcpartpicker as pcpp
try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 
from clint.textui import progress

class setUp:
    def __init__(self):
        pass
    def folderChq(self, str_vendor):
        #potentially add chipsets here
        str_cpwd = os.path.dirname(os.path.realpath(__file__))
        str_cpwd_full = os.path.join(str_cpwd,"BIOSHERE",str_vendor)
        if not os.path.exists(str_cpwd_full):
            os.makedirs(str_cpwd_full)
            print("Dir: \n" , str_cpwd_full ,  " \nCreated \n") 
        else:
            print("Dir: \n" , str_cpwd_full ,  " \nalready exists\n")

    def dl_Src_PCPP(self, vendor, modelData, allowedChipsets, allowedExtras):
        int_mobo_page_count = pcpp.productLists.totalPages("motherboard")
        print("Pages found: "+str(int_mobo_page_count))

        for page in range(1, int_mobo_page_count+1):
            skuName = pcpp.productLists.getProductList("motherboard", page)
            print("Collected page %d/%d" % (page,int_mobo_page_count))

            for model in skuName:
                str_fullsku = str(model["name"]).split(" ")
                str_modelsku = self.dl_Src_cleanStr(model["name"])
                if re.search(r'WI.FI|WIFI|AC|AX', str_modelsku, flags=re.IGNORECASE):
                    bool_wifi = True
                else:
                    bool_wifi = False
                print(model["name"]+"|wifi: "+str(bool_wifi))

                for x in range(len(allowedChipsets)):
                    regexString = (allowedChipsets[x]+allowedExtras)
                    #regexString = allowedChipsets[x]
                    if re.search(regexString,model["name"],flags=re.IGNORECASE):
                        vendorpcpp = (str_fullsku[0]).upper()
                        dict_dataDict = {'name':str_modelsku,'productURL':'','downloadURL':'','status':0,'vendor':vendorpcpp,'chipset':allowedChipsets[x],'wifi':bool_wifi}
                        #print(dict_dataDict)
                        self.generic_Sort(str_modelsku, vendorpcpp, modelData, vendor, dict_dataDict)

    def dl_Src_cleanStr(self,str_fullsku):
        model = str_fullsku.upper().replace(":","").replace(".", "-").replace(" ", "-").replace("(","").replace(")","").replace("-I-", "I-").replace("/","-")
        return model

    def generic_Sort(self,str_modelsku, vendor, modelData, vendorchq, dict_dataDict):
        try:
            moboKey = dict_dataDict['name']
           # print(dict_dataDict['vendor']+":"+str(vendorchq))
            if dict_dataDict['vendor'] in vendorchq:
                if not moboKey in modelData:   
                    modelData[moboKey] = dict_dataDict
                    print('Added: '+dict_dataDict['name'])
                else:
                    print(moboKey+" already in system...")
            else:
                print('Unsupported vendor: '+moboKey)

        except Exception as e: 
            print(e)
            print('Not Added: '+dict_dataDict['name'])

    def cleanup(self, cpath, index):
        try:
            print("Deleting "+cpath)
            os.remove(cpath)
        except: 
            print("Error in Deleting "+cpath)
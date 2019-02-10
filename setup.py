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
    def folderChq(self, company):
        #potentially add chipsets here
        cpwd = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(cpwd+"\\BIOSHERE\\"+company):
            os.makedirs(cpwd+"\\BIOSHERE\\"+company)
            print("Dir: \n" , cpwd+"\\BIOSHERE\\"+company ,  " \nCreated \n") 
        else:
            print("Dir: \n" , cpwd+"\\BIOSHERE\\"+company ,  " \nalready exists\n")

    def dl_Src_PCPP(self, vendor, modelData, allowedChipsets, allowedExtras):
        mobo_count = pcpp.productLists.totalPages("motherboard")
        print("Pages found: "+str(mobo_count))

        for page in range(1, mobo_count+1):
            skuName = pcpp.productLists.getProductList("motherboard", page)
            print("Collected page %d/%d" % (page,mobo_count))

            for model in skuName:
                fullsku = str(model["name"]).split(" ")

                for x in range(len(allowedChipsets)):
                    regexString = (allowedChipsets[x]+allowedExtras)
                    #regexString = allowedChipsets[x]
                    if re.search(regexString,model["name"],re.IGNORECASE):
                        vendorpcpp = (fullsku[0]).upper()
                        modelsku = self.dl_Src_cleanStr(model["name"])
                        dataDict = {'name':modelsku,'productURL':'','downloadURL':'','status':0,'vendor':vendorpcpp,'chipset':allowedChipsets[x]}
                        self.generic_Sort(modelsku, vendorpcpp, modelData, vendor, dataDict)

    def dl_Src_cleanStr(self,fullsku):
        model = fullsku.upper().replace(":","").replace(".", "-").replace(" ", "-").replace("(","").replace(")","").replace("-I-", "I-").replace("/","-")
        return model

    def generic_Sort(self,modelsku, vendor, modelData, vendorchq, dataDict):
        try:
            moboKey = dataDict['name']
            if dataDict['vendor'] in vendorchq:
                if not moboKey in modelData:   
                    modelData[moboKey] = dataDict
                    print('Added: '+dataDict['name'])
                else:
                    print(moboKey+" already in system...")
            else:
                print('Invalid vendor: '+moboKey)

        except Exception as e: 
            print(e)
            print('Not Added: '+dataDict['name'])

    def cleanup(self, cpath, index):
        try:
            print("Deleting "+cpath)
            os.remove(cpath)
        except: 
            print("Error in Deleting "+cpath)
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

    def dl_Src_PCPP(self, vendor, array, allowedChipsets, allowedExtras):
        mobo_count = pcpp.productLists.totalPages("motherboard")
        print("Pages found: "+str(mobo_count))
        for page in range(0, mobo_count):
            skuName = pcpp.productLists.getProductList("motherboard", page)
            print("Collected page "+ str(page))
            for model in skuName:
                fullsku = str(model["name"]).split(" ")
                for x in range(len(allowedChipsets)):
                    regexString = (allowedChipsets[x]+allowedExtras)
                    if re.search(regexString,model["name"],re.IGNORECASE):
                        vendorpcpp = (fullsku[0]).upper()
                        modelsku = self.dl_Src_cleanStr(model["name"])
                        self.generic_Sort(modelsku, vendorpcpp, array, vendor)

    def dl_Src_cleanStr(self,fullsku):
        model = fullsku.upper().replace(":","").replace(".", "-").replace(" ", "-").replace("(","").replace(")","").replace("-I-", "I-").replace("/","-")
        return model

    def generic_Sort(self,modelsku, vendor, array, vendorchq):
        for index in range(len(vendorchq)):
            if vendor == vendorchq[index]:
                array[index].append(modelsku)
                print("Sorted "+modelsku+" to "+vendorchq[index])
                break
            else:
                print("Could not Sort: "+modelsku+" to "+vendorchq[index])

    def arrClean(self, array1):
        for i in range (len (array1)-1):
            try:
                if array1[i] == array1[i+1]:
                    del array1[i]
            except:
                pass   
    def cleanup(self, modelarray, vendor):
        for i in range (len(modelarray)):
            cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/BIOSHERE/"+vendor+"/"+str(modelarray[i]).replace("/","-")+".zip"
            try:
                print("Deleting "+cpath)
                os.remove(cpath)
            except: 
                print("Error in Deleting "+cpath)
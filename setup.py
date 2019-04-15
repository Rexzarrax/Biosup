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

    def dl_Src_PCPP(self, arr_vendorchq, dict_modelData, arr_allowedChipsets, str_allowedExtras):
        int_mobo_page_count = pcpp.productLists.totalPages("motherboard")
        str_wifi_regex = r'WI.FI|WIFI|AC|AX'

        print("Pages found: "+str(int_mobo_page_count))
        #IF IT IS ALREADY IN THE SYSTEM, CHANGE THE FLAG
        for page in range(1, int_mobo_page_count+1):
            list_skus = pcpp.productLists.getProductList("motherboard", page)
            print("Collected page %d/%d" % (page,int_mobo_page_count))

            for model in list_skus:
                str_fullsku = str(model["name"]).split(" ")
                str_modelsku = self.dl_Src_cleanStr(model["name"])

                #check model for wifi
                if re.search(str_wifi_regex, str_modelsku, flags=re.IGNORECASE):
                    bool_wifi = True
                else:
                    bool_wifi = False
                #print(model["name"]+"|wifi: "+str(bool_wifi))

                for x in range(len(arr_allowedChipsets)):
                    str_regexString = (arr_allowedChipsets[x]+str_allowedExtras)
                    #str_regexString = arr_allowedChipsets[x]
                    if re.search(str_regexString,model["name"],flags=re.IGNORECASE):
                        str_vendor_from_pcpp = (str_fullsku[0]).upper()
                        dict_model_data = {'name':str_modelsku,'productURL':'','downloadURL':'','status':2,'vendor':str_vendor_from_pcpp,'chipset':arr_allowedChipsets[x],'wifi':bool_wifi}
                        #print(dict_model_data)
                        self.generic_Sort(str_modelsku, dict_modelData, arr_vendorchq, dict_model_data)
                    else:
                        print("Ignoring "+str_modelsku)
                
    def dl_Src_cleanStr(self,str_fullsku):
        model = str_fullsku.upper().replace(":","").replace(".", "-").replace(" ", "-").replace("(","").replace(")","").replace("-I-", "I-").replace("/","-")
        return model

    def generic_Sort(self,str_modelsku, dict_modelData, arr_vendorchq, dict_model_data):
        try:
            str_moboKey = dict_model_data['name']
           # print(dict_model_data['vendor']+":"+str(arr_vendorchq))
            if dict_model_data['vendor'] in arr_vendorchq:
                if not str_moboKey in dict_modelData:   
                    dict_modelData[str_moboKey] = dict_model_data
                    dict_modelData[str_moboKey]['status'] = 1
                    print('Added: '+dict_model_data['name'])
                else:
                    dict_modelData[str_moboKey]['status'] = 1
                    print(str_moboKey+" already in system...")
            else:
                print('Unsupported vendor: '+str_moboKey)

        except Exception as e: 
            print(e)
            print('Not Added: '+dict_model_data['name'])

    def cleanup(self, str_cpath, index):
        try:
            print("Deleting "+str_cpath)
            os.remove(str_cpath)
        except: 
            print("Error in Deleting "+str_cpath)
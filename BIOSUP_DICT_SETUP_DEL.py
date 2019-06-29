import os
import json
import random
import requests
import re
from BIOSUP_WEB_SCRAPER import web_scraper
#from pcpartpickerapi import part_lists as pcpp
#from part_lists import as pcpp
try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 
from clint.textui import progress

class setUp:
    def __init__(self):
        self.str_github_pull = "https://raw.githubusercontent.com/Rexzarrax/Motherboard_Model_Names/master/motherboard_sku_data.txt"
    def folderChq(self, str_vendor):
        #potentially add chipsets here
        str_cpwd = os.path.dirname(os.path.realpath(__file__))
        str_cpwd_full = os.path.join(str_cpwd,"BIOSHERE",str_vendor)
        if not os.path.exists(str_cpwd_full):
            os.makedirs(str_cpwd_full)
            print("Dir: \n" , str_cpwd_full ,  " \nCreated \n") 
        else:
            print("Dir: \n" , str_cpwd_full ,  " \nalready exists\n")
    
    def dict_generation(self, arr_vendorchq, dict_modelData, arr_allowedChipsets, str_allowedExtras, list_skus):
        str_wifi_regex = r'WI.FI|WIFI|AC|AX'
        print(str(list_skus))
        for model in list_skus:
            print(str(model))
            #str_fullsku = str(model["name"]).split(" ")
            str_fullsku = str(model["name"])
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
                    try:
                        str_vendor = model['vendor']
                    except:
                        pass
                    dict_model_data = {'name':str_modelsku,'productURL':'','downloadURL':'','status':0,'vendor':str_vendor,'chipset':arr_allowedChipsets[x],'wifi':bool_wifi}
                    print(dict_model_data)
                    self.generic_Sort(str_modelsku, dict_modelData, arr_vendorchq, dict_model_data)


    def dl_src_github(self,arr_vendorchq, dict_modelData, arr_allowedChipsets, str_allowedExtras):
        arr_models = web_scraper.get_page(self.str_github_pull).splitlines()
        random.shuffle(arr_models)
        dict_models = []
        print(str(arr_models))
        for model in arr_models:
            arr_str_model = model.split('-')
            str_model_vendor = arr_str_model[0]
            dict_models.append({'name':model,'vendor':str_model_vendor})
        self.dict_generation(arr_vendorchq, dict_modelData, arr_allowedChipsets, str_allowedExtras, dict_models)

    # def dl_Src_PCPP(self, arr_vendorchq, dict_modelData, arr_allowedChipsets, str_allowedExtras):
    #     #int_mobo_page_count = pcpp.list_info("motherboard")["page_count"]
    #     int_mobo_page_count = pcpp.list_page_count("motherboard")

    #     print("Pages found: "+str(int_mobo_page_count))
    #     #IF IT IS ALREADY IN THE SYSTEM, CHANGE THE FLAG
    #     for int_page in range(1, int_mobo_page_count+1):
    #         list_skus = pcpp.get_list("motherboard", page=int_page)
    #         print("Collected page %d/%d" % (int_page,int_mobo_page_count))
    #     self.dict_generation(arr_vendorchq, dict_modelData, arr_allowedChipsets, str_allowedExtras, list_skus)
    #         
                
    def dl_Src_cleanStr(self,str_fullsku):
        model = str_fullsku.upper().replace(":","").replace(".", "-").replace(" ", "-").replace("(","").replace(")","").replace("-I-", "I-").replace("/","-")
        return model

    def generic_Sort(self,str_modelsku, dict_modelData, arr_vendorchq, dict_model_data):
        try:
            str_moboKey = dict_model_data['name']
           # print(dict_model_data['vendor']+":"+str(arr_vendorchq))
           #put ignore state some how here
            if dict_model_data['vendor'] in arr_vendorchq:
                if not str_moboKey in dict_modelData:   
                    dict_modelData[str_moboKey] = dict_model_data
                    obj_print.print_msg('Added: '+dict_model_data['name'])
                    dict_modelData[str_moboKey]['status'] = 1
                else:
                    dict_modelData[str_moboKey]['status'] = 1
                    obj_print.print_msg(str_moboKey+" already in system...")
                
            else:
                obj_print.print_msg('Unsupported vendor: '+str_moboKey)

        except Exception as e: 
            obj_print.print_msg(e)
            obj_print.print_msg('Not Added: '+dict_model_data['name'])

    def cleanup(self, str_cpath, index):
        try:
            obj_print.print_msg("Deleting "+str_cpath)
            os.remove(str_cpath)
        except: 
            obj_print.print_msg("Error in Deleting "+str_cpath)
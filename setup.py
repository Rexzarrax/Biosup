import os
import json
import requests
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
        cpwd = os.path.dirname(os.path.realpath(__file__))+"/"
        if not os.path.exists(cpwd+company):
            os.mkdir(cpwd+company)
            print("Dir: \n" , cpwd+company ,  " \nCreated \n") 
        else:
            print("Dir: \n" , cpwd+company ,  " \nalready exists\n")

    def dlSrcPCPP(self, vendor, mysetup):
        #need to work out a system to filter unwanted skus, also save this list due to taking AGES to fix
        mobo_count = pcpp.productLists.totalPages("motherboard")
        print("Total Mb pages:", mobo_count)

        # Pull info from page 1 of CPUs
        for page in range(0, mobo_count):
            skuName = pcpp.productLists.getProductList("motherboard", page)
            # Print the names and prices of all the CPUs on the page
            for mobo in skuName:
                fullsku = str(mobo["name"]).split(" ")
                vendorpcpp = (fullsku[0]).upper()
                model = fullsku[1]
                

    def innerHTML(self, element):
        return (element.encode_contents()).decode("utf-8").replace("SKU: ","").strip().replace(" ","-")

    def dl_Src_PLE_API(self, vendor, array):
        url = "https://www.ple.com.au/api/getItemGrid"
        payload = {'Header': '','Content-Type':application/json, 'Body':{"InventoryCategoryId":302}}
        r = requests.post(url, data=payload)
        data = json.loads(r)
        ['data']
        [obj for obj in data if data['ManufacturerName']==vendor]
        


    def dlSrcPLE(self, myGetWeb, vendor, array):
        site = "https://www.ple.com.au/Motherboards/"+vendor
        raw_html = myGetWeb.simple_get(site)
        html = BeautifulSoup(raw_html, 'html.parser')
        filter1 = html.find_all("div", {"class":"pg_manufacturermodel"})
        print("Getting: "+site)
        
        for div in filter1:
            model = str(self.innerHTML(div)).replace(" ","-")
            array.append(model)
 
    def arrClean(self, array1):
        for i in range (len (array1)-1):
            try:
                if array1[i] == array1[i+1]:
                    del array1[i]
            except:
                pass   
    def cleanup(self, modelarray, vendor):
            for i in range (len(modelarray)):
                cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/"+vendor+"/"+str(modelarray[i]).replace("/","-")+".zip"
                try:
                    print("Deleting "+cpath)
                    os.remove(cpath)
                except: 
                    print("Err in Deleting "+cpath)
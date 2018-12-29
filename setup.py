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

    def dl_Src_PCPP(self, vendor, array):
        mobo_count = pcpp.productLists.totalPages("motherboard")
        for page in range(0, mobo_count):
            skuName = pcpp.productLists.getProductList("motherboard", page)
            print("Collected page "+ str(page))
            for mobo in skuName:
                fullsku = str(mobo["name"]).split(" ")
                print("Found:"+ str(fullsku))
                vendorpcpp = (fullsku[0]).upper()
                model = "-"
                for strs in fullsku:
                    model += "-"+strs 
                if vendorpcpp == vendor:
                    array.append(model.replace("--",""))

    def dl_Src_PLE_API(self, vendor, array):
        url = "https://www.ple.com.au/api/getItemGrid"
        headers = ''
        payload = {'Content-type':'application/json','Body':{"InventoryCategoryId":'302'}}
        r = requests.post(url, data=payload, headers=headers)

        print("Resp Code: "+str(r.status_code))
        #data = json.loads(r)['data']
        data = r.json()
        print(str(data))
        if r.status_code == 200:
            [obj for obj in data if data['ManufacturerName']==vendor]
            for objectmodel in data:
                print(str(objectmodel))
                if vendor == "ASUS":
                    array.append(objectmodel)
                elif vendor == "GIGABYTE":
                    array.append(objectmodel)
                elif vendor == "MSI":
                    array.append(objectmodel)
                elif vendor == "ASROCK":
                    array.append(objectmodel)
                else:
                    print("Error in PLE API")
        else:
            print("Error in Request, code: "+r.status_code)


    #def dlSrcPLE(self, myGetWeb, vendor, array):
    #    site = "https://www.ple.com.au/Motherboards/"+vendor
    #    print("Getting: "+site)
    #    raw_html = myGetWeb.simple_get(site)
    #    html = BeautifulSoup(raw_html, 'html.parser')
    #    filter1 = html.find_all("div", {"class":"pg_manufacturermodel"})
    #    
    #    
    #    for div in filter1:
    #        print(div)
    #        model = str(self.innerHTML(div)).replace(" ","-")
    #        array.append(model.replace)
 
    def innerHTML(self, element):
        return (element.encode_contents()).decode("utf-8").replace("SKU: ","").strip().replace(" ","-")

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
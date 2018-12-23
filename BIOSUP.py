import os
import sys
import re
import contextlib
import requests
import zipfile

from clint.textui import progress

from PCPartPicker_API import pcpartpicker as pcpp

try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 

from selenium import webdriver

#stores motherboard data
class moboData:
    def __init__(self, mysetup, myGetWeb, vendor):
        #need to make variable, based on length of vendor array in main
        self.asrockArr = []
        self.asusArr = []
        self.gigabyteArr = []
        self.msiArr = []

        self.allVenArr = [self.asrockArr, self.asusArr, self.gigabyteArr, self.msiArr]

        for ven in range(len(self.allVenArr)):
            try:
                #mysetup.dlSrcPCPP(vendor[ven], mysetup)
                mysetup.dlSrcPLE(myGetWeb, vendor[ven], self.allVenArr[ven])
            except:
                pass
            

class unzip:
    def __init__(self):
        pass
    def deZip(self, file2unzip, folder2extract2):
        try:
            unzip = zipfile.ZipFile(file2unzip)
            unzip.extractall(folder2extract2)     
            unzip.close()
            #os.remove(file2unzip)
        except requests.exceptions.RequestException as e:
            self.log_error('Error during unzipping to '+str(e))


#Collects the skus of the various mobo
class gethtml:
    def __init__(self):
        pass

    def simple_get(self, url):
        try:
            with contextlib.closing(requests.get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return "Not Valid HTML"

        except requests.exceptions.RequestException as e:
            print("Err: "+str(url) + str(e))
            return None


    def is_good_response(self, resp):
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 
                and content_type is not None 
                and content_type.find('html') > -1)


    def log_error(e):
        print(e)

#get the list of motherboard names from file
#and saves them to Array
#creates the file structure to easily find BIOS'
class inputfiles:
    #create state machine that returnes the name of the text file
    def genCompnay(self, myData, fileObject):
        for line in fileObject:
            myData.append(line.rstrip())
            print(line.rstrip() + " -> "+str(fileObject.name.split('Biosup/', 1)[-1]).strip(".txt")+"Arr")

    def getFile(self, filename):
        path = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))+filename
        fileObject = open(path)
        return fileObject

    #determine the company to get the company model file
    def StartHere(self, myData, filename, companyint):
        fileObject = self.getFile(filename)
        self.genCompnay(myData, fileObject)

    def __Init__(self):
        pass

#class holds methods for downloading the BIOS from a vendor
class bioufiDL:
    #Download bios from Asrock    
    def urlBuilderAsrock(self,myGetWeb, mymodel, urlchq, cpath):
        #cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/ASROCK/"+str(mymodel).replace("/","-")+".zip"
        #get html page
        print("Getting Src...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq)).replace("index.asp","")+"BIOS.html"
            print("Src URL: "+prodURL)
            print("Getting URL...")
            html_page = myGetWeb.simple_get(prodURL)
            #select only the url
            soup_html = BeautifulSoup(html_page, "html5lib")
            for link in soup_html.find_all('a', attrs={'href': re.compile("^http://asrock.pc.cdn.bitgravity.com/BIOS/")}):
                print("Found the URL:", link['href'])
                if self.dlBIOS(link, cpath):
                    break        
        else:
            print("already Downloaded")
    #Download bios from Asus
    def urlBuilderAsus(self,myGetWeb, mymodel, urlchq, cpath):
        print("Getting Src...")
        #get html page
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq))
            print("Src URL: "+prodURL)
            print("Getting URL...")
            soup_html = self.getwebwithjs(prodURL)
            #print(soup_html)
            for link in soup_html.find_all('a', attrs={'href': re.compile("^https://dlcdnets.asus.com/pub")}):
                print("Found the URL:", link['href'])
                if self.dlBIOS(link, cpath):
                    break  
                else:
                    pass      
        else:
            print("already Downloaded\n")

    #download BIOS from Gigabyte
    def urlBuilderGigabyte(self,myGetWeb, mymodel, urlchq, cpath):
        print("Getting Src...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq)+"#support-dl-bios")
            print("Src URL: "+prodURL)
            print("Getting URL...")
            soup_html = self.getwebwithjs(prodURL)
            #print(soup_html)
            for link in soup_html.find_all('a', attrs={'href': re.compile("^http://download.gigabyte.asia/FileList/BIOS")}):
                print("Found the URL:", link['href'])
                if self.dlBIOS(link, cpath):
                    break  
                else:
                    pass                          
        else:
            print("already Downloaded\n")

    #download BIOS from MSI
    def urlBuilderMSI(self,myGetWeb, mymodel, urlchq, cpath):
        print("Getting Src...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq)+"#down-bios")
            print("Src URL: "+prodURL)
            print("Getting URL...")
            #select only the url  
            soup_html = self.getwebwithjs(prodURL)
            #print(soup_html)
            for link in soup_html.find_all('a', attrs={'href': re.compile("^http://download.msi.com/bos")}):
                print("Found the URL:", link['href'])
                if self.dlBIOS(link, cpath):
                    break  
                else:
                    pass      
        else:
            print("already Downloaded\n")
#Downloads and saves the zipped bios file to the cpath location
#cpath: the path to the file
#link: the url of the BIOS
    def dlBIOS(self, link, cpath):
        try:             
            r = requests.get(link.get('href'), allow_redirects=True)
            print("DL and Save to "+cpath)
            with open(cpath, 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
            if os.path.exists(cpath):
                print("BIOS Successfully Downloaded...")
                return True
                
            else:
                print("Download Failed...\n")
                return False
                
        except Exception as e:
            print("Error: "+str(e))

    def getwebwithjs(self, link):
        Firefox = True

        if Firefox:
            #FireFox headless
            options = webdriver.firefox.options.Options()
            options.add_argument('-headless')
            driver = webdriver.Firefox(options=options)
            driver.get(link)
        else:
            #Chrome Headless
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=options)
        
        temp = BeautifulSoup(driver.page_source, "html5lib") #page_source fetches page after rendering is complete
        driver.quit()
        return temp
    
    def searchforlink(self, mymodel, urlchq):
        for j in search(mymodel+" bios", tld="co.in", num=10, stop=1, pause=2): 
        #for j in search(mymodel+" BIOS", tld="co.in", num=10, stop=1, pause=2): 
            #print(mymodel+": "+j)
            if re.search(urlchq, j, re.IGNORECASE):
                return j

    def __Init__(self):
        pass

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

    def dlSrcPLE(self, myGetWeb, vendor, array):
        site = "https://www.ple.com.au/Motherboards/"+vendor
        raw_html = myGetWeb.simple_get(site)
        html = BeautifulSoup(raw_html, 'html.parser')
        filter1 = html.find_all("div", {"class":"pg_manufacturermodel"})
        print("Getting: "+site)
        
        for div in filter1:
            array.append(self.innerHTML(div))
            #print(self.innerHTML(div))    
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
    
#initial checks and basic file creation
def main():
    print("----------BIOSUP----------")
    print("Initialising...")

    #config
    clean = False

    vendor = ["ASROCK","ASUS", "GIGABYTE", "MSI"]
    #vendor = ["MSI"]

    mysetup = setUp()
    myGetWeb = gethtml()
    myData = moboData(mysetup, myGetWeb, vendor)  
    myI = inputfiles()
    getBIO = bioufiDL()
    dezip = unzip()

    print(vendor)

    #create folders
    for ven1 in range(len(vendor)):
        mysetup.folderChq(vendor[ven1])
    
    print("Sourcing models...")
    #Sort the arrays ready for further processing+delete duplicate entries
    for ven2 in range(len(vendor)):
        myData.allVenArr[ven2].sort()
        mysetup.arrClean(myData.allVenArr[ven2])
        print("\n"+str(myData.allVenArr[ven2])+"\n")
    #Get models
    for modelStr in myData.asusArr:   
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/ASUS/"+str(modelStr).replace("/","-")+".zip"  
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderAsus(myGetWeb, modelStr ,"^https:\/\/www\.asus\.com", cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")
    for modelStr in myData.gigabyteArr:
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/GIGABYTE/"+str(modelStr).replace("/","-")+".zip"  
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderGigabyte(myGetWeb, modelStr ,"^https:\/\/www\.gigabyte\.com", cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")
    for modelStr in myData.msiArr:   
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/MSI/"+str(modelStr).replace("/","-")+".zip"
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderMSI(myGetWeb, modelStr ,"^https:\/\/www\.msi\.com", cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")
    for modelStr in myData.asrockArr: 
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/ASROCK/"+str(modelStr).replace("/","-")+".zip"  
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderAsrock(myGetWeb, modelStr,"^https:\/\/www\.asrock\.com\/mb", cpath)
        print("Unzipping: "+cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")


    if clean:
        print("Running Cleanup...")
        for v in range(len(vendor)):
            mysetup.cleanup(myData.allVenArr[v], vendor[v])
            


    print("Finished...")

if __name__ == "__main__":
    main()


#extra scopes:
#->select src, either PLE or PCPP
#-> generate local lists to reduce dl time in future
#-> cli menu system
#-> options for specific sources/vendors

#planned scopes:
#-> config file

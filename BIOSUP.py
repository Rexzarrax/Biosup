import os
import sys
import re
import contextlib
import requests
import zipfile

from PCPartPicker_API import pcpartpicker as pcpp

try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 

#from PyQt4.QtGui import QApplication
#from PyQt4.QtCore import QUrl
#from PyQt4.QtWebKit import QWebPage


#extra scopes:
#->select src, either PLE or PCPP
#-> generate local lists to reduce dl time in future
#-> cli menu system

#planned scopes:
#->unzip bios' ready for reading by flash software
#-> config file

#stores motherboard data
class moboData:
    def __init__(self, mysetup, myGetWeb, vendor):
        #COMBINE INTO 2D ARRAY IN FUTURE
        self.asrockArr = []
        self.asusArr = []
        self.gigabyteArr = []
        self.msiArr = []

        self.allVenArr = [self.asrockArr, self.asusArr, self.gigabyteArr, self.msiArr]

        for ven in range(len(self.allVenArr)):
            mysetup.dlSrcPLE(myGetWeb, vendor[ven], self.allVenArr[ven])

class unzip:
    def __init__(self):
        pass
    def deZip(self, file2unzip, folder2extract2):
        unzip = zipfile.ZipFile(file2unzip)
        unzip.extractall(folder2extract2)
        
        unzip.close()

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
            self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))
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

#creates the URL to then download the files to
class bioufiDL:
    #Download bios from Asus
    def urlBuilderAsus(self,myGetWeb, mymodel, urlchq):
        formatModel= str(mymodel).replace("(","").replace(")","")
        print(formatModel)
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/ASUS/"+formatModel+".zip"
        #get html page
        if not os.path.exists(cpath):
            prodURL = "https://www.asus.com/us/Motherboards/"+formatModel+"/HelpDesk_BIOS/"
            print("Src URL: "+prodURL)
                           
            
        else:
            print("already Downloaded\n")
    #Download bios from Asrock    
    def urlBuilderAsrock(self,myGetWeb, mymodel, urlchq):
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/ASROCK/"+str(mymodel).replace("/","-")+".zip"
        #get html page
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq)).replace("index.asp","BIOS.html")
            print("Src URL: "+prodURL)
            html_page = myGetWeb.simple_get(prodURL)
            #select only the url
            soup_html = BeautifulSoup(html_page, "html5lib")
            for link in soup_html.find_all('a', attrs={'href': re.compile("^http://")}):
                print("Found the URL:", link['href'])
                if self.dlBIOS(link, cpath):
                    break        
        else:
            print("already Downloaded\n")

    #download BIOS from Gigabyte
    def urlBuilderGigabyte(self,myGetWeb, mymodel, urlchq):
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/GIGABYTE/"+str(mymodel).replace("/","-")+".zip"
        #get html page
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq)+"#support-dl-bios")
            print("Src URL: "+prodURL)
            html_page = myGetWeb.simple_get(prodURL)
            #select only the url  
            soup_html = BeautifulSoup(html_page, "html5lib")
            for myDiv in soup_html.find_all('div', attrs={'class':'div-table'}):
                print(myDiv.text)
                for link in myDiv.find_all('a', attrs={'href': re.compile("^http://")}):
                    print("Found the URL:", link['href'])
                    if self.dlBIOS(link, cpath):
                        break  
                    else:
                        pass                     
        else:
            print("already Downloaded\n")
        pass
    #download BIOS from MSI
    def urlBuilderMSI(self,myGetWeb, mymodel, urlchq):
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/MSI/"+str(mymodel).replace("/","-")+".zip"
        #get html page
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel+"bios", urlchq)+"#down-bios")
            print("Src URL: "+prodURL)
            html_page = myGetWeb.simple_get(prodURL)
            #select only the url  
            soup_html = BeautifulSoup(html_page, "html5lib")
            for myDiv in soup_html.find_all('div', attrs={'class':'row spec'}):
                for link in myDiv.find_all('a', class_={'href': re.compile("^http://download.msi.com")}):
                    print("Found the URL:", link['href'])
                    if self.dlBIOS(link, cpath):
                        break  
                    else:
                        pass
                      
        else:
            print("already Downloaded\n")
        pass

    def dlBIOS(self, link, cpath):
        try:             
            r = requests.get(link.get('href'), allow_redirects=True)
            
            print("DL and Save to "+cpath)
            open(cpath , 'wb').write(r.content)
            if os.path.exists(cpath):
                print("BIOS Successfully Downloaded...\n")
                return True
                
            else:
                print("Download Failed...\n")
                return False
                
        except Exception as e:
            print("Error: "+str(e))
            
    
    def searchforlink(self, mymodel, urlchq):
        for j in search(mymodel, tld="co.in", num=10, stop=1, pause=2): 
            if re.search(urlchq, j):
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

    def dlSrcPCPP(self):
        mobo_count = pcpp.productLists.totalPages("motherboard")
        print("Total Mobo pages:", mobo_count)

        # Pull info from page 1 of CPUs
        for page in range(0, mobo_count):
            skuName = pcpp.productLists.getProductList("motherboard", page)
            # Print the names and prices of all the CPUs on the page
            for mobo in skuName:
                fullsku = str(mobo["name"]).split(" ")
                vendor = fullsku[0]
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

class cleanArr:
    def arrClean(self, array1):
        for i in range (len (array1)-1):
            try:
                if array1[i] == array1[i+1]:
                    del array1[i]
            except:
                pass
#initial checks and basic file creation
def main():
    print("----------BIOSUP----------")
    print("Initialising...")

    vendor = ["ASROCK","ASUS", "GIGABYTE", "MSI"]

    mysetup = setUp()
    myGetWeb = gethtml()
    myData = moboData(mysetup, myGetWeb, vendor)  
    myI = inputfiles()
    cleanArr1 = cleanArr()
    getBIO = bioufiDL()

    #create folders
    for ven1 in range(len(vendor)):
        mysetup.folderChq(vendor[ven1])
    
    #import models from local files
    #myI.StartHere(myData.asrockArr, "/Sources/asrock.txt", 1)
    #myI.StartHere(myData.asusArr, "/Sources/asus.txt", 2)
    #myI.StartHere(myData.gigabyteArr, "/Sources/gigabyte.txt", 4)
    #myI.StartHere(myData.msiArr, "/Sources/msi.txt", 3)
    #Download skus from PLE website
    print("Sourcing models...")
    #Sort the arrays ready for further processing+delete duplicate entries
    for ven2 in range(len(vendor)):
        myData.allVenArr[ven2].sort()
        cleanArr1.arrClean(myData.allVenArr[ven2])
        print("\n"+str(myData.allVenArr[ven2])+"\n")

    for modelStr in myData.asrockArr:   
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderAsrock(myGetWeb, modelStr ,"^https:\/\/www\.asrock\.com")
    for modelStr in myData.msiArr:   
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderMSI(myGetWeb, modelStr ,"^https:\/\/www\.msi\.com")
    for modelStr in myData.gigabyteArr:   
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderGigabyte(myGetWeb, modelStr ,"^https:\/\/www\.gigabyte\.com")
    for modelStr in myData.asusArr:   
        print("Getting "+modelStr+"'s BIOS...")
        getBIO.urlBuilderAsus(myGetWeb, modelStr ,"^https:\/\/www\.asus\.com")

    print("Finished...")

if __name__ == "__main__":
    main()



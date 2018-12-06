import zipfile
import os

import contextlib
import requests
from bs4 import BeautifulSoup


#extra scopes:
#use PLE website to source motherboards to get BIOS' for
#sort into folders for company

#unzip bios' ready for reading by flash software
#stores motherboard data
class moboData:
    def __init__(self):
        self.asrockArr = []
        self.asusArr = []
        self.gigabyteArr = []
        self.msiArr = []

class unzip:
    def __init__(self):
        pass
    def deZip(self):
        unzip = zipfile.ZipFile(file2unzip)
        unzip.extractall(folder2extract2)
        
        unzip.close()

#Collects the skus of the various mobo
class getskuandsave:
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
        
class dlModels:
    def __init__(self):
        pass

    def innerHTML(self, element):
        return (element.encode_contents()).decode("utf-8").replace("SKU: ","").strip().replace(" ","-")

    def getsku(self, myGetWeb, url, array):
        raw_html = myGetWeb.simple_get(url)
        html = BeautifulSoup(raw_html, 'html.parser')
        filter1 = html.find_all("div", {"class":"pg_manufacturermodel"})
        print("Getting: "+url)
        
        for div in filter1:
            array.append(self.innerHTML(div))
            #print(self.innerHTML(div))


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
    def urlBuilderAsus(self, model):
        url = "https://www.asus.com/au/Motherboards/"+model+"/HelpDesk_BIOS/"
        pass
    def urlBuilderAsrock(self):
        pass
    def urlBuilderGigabyte(self):
        pass
    def urlBuilderMSI(self):
        pass

    def __Init__(self):
        pass
class setUp:
    def folderChq(self, company):
        cpwd = os.path.dirname(os.path.realpath(__file__))+"/"
        if not os.path.exists(cpwd+company):
            os.mkdir(cpwd+company)
            print("Dir: " , company ,  " Created ") 
        else:
            print("Dir: " , company ,  " already exists")

    def printmodels(self, myData):
        print("Asrock: "+str(myData.asrockArr)+"\n") 
        print("Asus: "+str(myData.asusArr)+"\n")
        print("MSI: "+str(myData.msiArr)+"\n")
        print("Gigabyte: "+str(myData.gigabyteArr)+"\n")


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

    mysetup = setUp()
    myData = moboData()  
    myI = inputfiles()
    myGetWeb = getskuandsave()
    myO = dlModels()
    cleanArr1 = cleanArr()
    #create folders
    mysetup.folderChq("ASROCK")
    mysetup.folderChq("GIGABYTE")
    mysetup.folderChq("ASUS")
    mysetup.folderChq("MSI")
    #import models from local files
    #myI.StartHere(myData.asrockArr, "/Sources/asrock.txt", 1)
    #myI.StartHere(myData.asusArr, "/Sources/asus.txt", 2)
    #myI.StartHere(myData.gigabyteArr, "/Sources/gigabyte.txt", 4)
    #myI.StartHere(myData.msiArr, "/Sources/msi.txt", 3)
    #Download skus from PLE website
    myO.getsku(myGetWeb, "https://www.ple.com.au/Motherboards/ASRock", myData.asrockArr)
    myO.getsku(myGetWeb, "https://www.ple.com.au/Motherboards/Gigabyte", myData.gigabyteArr)
    myO.getsku(myGetWeb, "https://www.ple.com.au/Motherboards/ASUS", myData.asusArr)
    myO.getsku(myGetWeb, "https://www.ple.com.au/Motherboards/MSI", myData.msiArr)
    #Sort the arrays ready for further processing
    myData.asrockArr.sort()
    myData.asusArr.sort()
    myData.gigabyteArr.sort()
    myData.msiArr.sort()
    #delete duplicate entries
    cleanArr1.arrClean(myData.asrockArr)
    cleanArr1.arrClean(myData.asusArr)
    cleanArr1.arrClean(myData.gigabyteArr)
    cleanArr1.arrClean(myData.msiArr)
    #print results
    mysetup.printmodels(myData)

if __name__ == "__main__":
    main()



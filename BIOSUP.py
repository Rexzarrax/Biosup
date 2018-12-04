import zipfile
import os

import contextlib
import requests
from bs4 import BeautifulSoup


#extra scopes:
#use PLE website to source motherboards to get BIOS' for
#sort into folders for company

#unzip bios' ready for reading by flash software
class unzip:
    
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


    def is_good_response(resp):
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 
                and content_type is not None 
                and content_type.find('html') > -1)


    def log_error(e):
        print(e)

#stores motherboard data2
class moboData:
    def __init__(self):
        self.asrockArr = []
        self.asusArr = []
        self.gigabyteArr = []
        self.msiArr = []
        
        

#get the list of motherboard names from file
#and saves them to Array
#creates the file structure to easily find BIOS'
class IO:
    def asrock(self, myData, fileObject):
        for line in fileObject:
            myData.append(line.rstrip())
            print(line.rstrip() + " -> asrockArr")

    def asus(self,myData, fileObject):
        for line in fileObject:
            myData.append(line.rstrip())
            print(line.rstrip() + " -> asusArr")

    def msi(self,myData, fileObject):
        for line in fileObject:
            myData.append(line.rstrip())
            print(line.rstrip() + " -> msiArr")

    def gigabyte(self,myData, fileObject):
        for line in fileObject:
            myData.append(line.rstrip())
            print(line.rstrip() + " -> gigabyteArr")

    def getFile(self, filename):
        path = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))+filename
        fileObject = open(path)
        return fileObject

    #determine the company to get the company model file
    def StartHere(self, myData, filename, companyint):
        if companyint == 1:
            fileObject = self.getFile(filename)
            self.asrock(myData, fileObject)
        elif companyint == 2:
            fileObject = self.getFile(filename)
            self.asus(myData, fileObject)
        elif companyint == 3:
            fileObject = self.getFile(filename)
            self.msi(myData, fileObject)
        elif companyint == 4:
            fileObject = self.getFile(filename)
            self.gigabyte(myData, fileObject)
        else:
            print("Error in case statement")
    def __Init__(self):
        pass

    
#load models from website(wait till website updates)       
#class webFetch:


class setUp:
    def folderChq(self, company):
        if not os.path.exists(company):
            os.mkdir(company)
            print("Dir: " , company ,  " Created ") 
        else:
            print("Dir: " , company ,  " already exists")

    def printmodels(self, myData):
        print("Asrock: "+str(myData.asrockArr)) 
        print("Asus: "+str(myData.asusArr))
        print("MSI: "+str(myData.msiArr))
        print("Gigabyte: "+str(myData.gigabyteArr))


#initial checks and basic file creation
def main():
    print("----------BIOSUP----------")
    print("Initialising...")

    mysetup = setUp()
    myData = moboData()  
    myIO = IO()

    mysetup.folderChq("ASROCK")
    mysetup.folderChq("GIGABYTE")
    mysetup.folderChq("ASUS")
    mysetup.folderChq("MSI")

    myIO.StartHere(myData.asrockArr, "/asrockmodel.txt", 1)
    myIO.StartHere(myData.asusArr, "/asusmodel.txt", 2)
    myIO.StartHere(myData.gigabyteArr, "/gigabytemodel.txt", 4)
    myIO.StartHere(myData.msiArr, "/msimodel.txt", 3)

    mysetup.printmodels(myData)

if __name__ == "__main__":
    main()



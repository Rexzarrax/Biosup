import zipfile
import os

#extra scopes:
#use PLE website to source motherboards to get BIOS' for
#sort into folders for company

#unzip bios' ready for reading by flash software
class unzip:
    
    def deZip(self):
        unzip = zipfile.ZipFile(file2unzip)
        unzip.extractall(folder2extract2)
        
        unzip.close()

#downloads the bios from the internet
class download:
    #initialiser
    pass

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
    #load file to get models

    def asrock(self, myData, fileObject):
        for line in fileObject:
            myData.append(line)
            print("Adding "+ line + " to asrockArr")

    def asus(self,myData, fileObject):
        for line in fileObject:
            myData.append(line)
            print("Adding "+ line + " to asusArr")

    def msi(self,myData, fileObject):
        for line in fileObject:
            myData.append(line)
            print("Adding "+ line + " to msiArr")

    def gigabyte(self,myData, fileObject):
        for line in fileObject:
            myData.append(line)
            print("Adding "+ line + " to gigabyteArr")

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

#initial checks and basic file creation
def main():
    print("----------BIOSUP----------")
    print("Initialising...")
    mysetup = setUp()
    mysetup.folderChq("ASROCK")
    mysetup.folderChq("GIGABYTE")
    mysetup.folderChq("ASUS")
    mysetup.folderChq("MSI")

    myData = moboData()
    myIO = IO()
    myIO.StartHere(myData.asrockArr, "/asrockmodel.txt", 1)
    myIO.StartHere(myData.asusArr, "/asusmodel.txt", 2)
    myIO.StartHere(myData.gigabyteArr, "/gigabytemodel.txt", 4)
    myIO.StartHere(myData.msiArr, "/msimodel.txt", 3)

    print("Asrock: "+str(myData.asrockArr)) 
    print("Asus: "+str(myData.asusArr))
    print("MSI: "+str(myData.msiArr))
    print("Gigabyte: "+str(myData.gigabyteArr))


if __name__ == "__main__":
    main()



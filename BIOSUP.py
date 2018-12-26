import sys
import requests
import os

from Unzip import unzip
from getHTML import gethtml
from biosDL import bioufiDL
from setup import setUp
from inputFiles import inputfiles

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
    
#initial checks and basic file creation
def main():
    print("----------BIOSUP----------")
    print("Initialising...")

    #config
    clean = True

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
        getBIO.urlBuilderAsus(myGetWeb, modelStr ,"^https:\/\/www\.asus\.com\/", cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")
    for modelStr in myData.gigabyteArr:
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/GIGABYTE/"+str(modelStr).replace("/","-")+".zip"  
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderGigabyte(myGetWeb, modelStr ,"^https:\/\/www\.gigabyte\.com\/Motherboard\/", cpath)
        dezip.deZip(cpath, cpath.strip(".zip"))
        print("All actions Attempted, moving to next BIOS...\n")
    for modelStr in myData.msiArr:   
        cpath = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/MSI/"+str(modelStr).replace("/","-")+".zip"
        print(modelStr+"'s BIOS...")
        getBIO.urlBuilderMSI(myGetWeb, modelStr ,"^https:\/\/www\.msi\.com\/Motherboard\/support\/", cpath)
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

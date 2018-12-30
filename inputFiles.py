import os
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

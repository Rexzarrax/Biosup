import os
import time

class datastatistics:
    def __init__(self):
        self.timeEnd = 0
        self.timeDelta = 0
        self.Failed = []
        self.timeStart = time.time()
        self.successStr = []

    def statistics(self, myData, vendor, ven):
        intModelCount = 0
        for model1 in myData.allVenArr[ven]:
            cpathchq = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/"+vendor+"/"+str(model1)+".zip"
            if os.path.exists(cpathchq):
                intModelCount += 1
            else:
                self.Failed.append("Failed to get: "+vendor+"|"+model1)
        self.successStr.append(vendor+": Successful Download's: "+str(intModelCount)+"/"+str(len(myData.allVenArr[ven])))
            
        self.timeEnd = time.time()
        self.timeDelta = int((self.timeEnd - self.timeStart)/60)
    
    def printstat(self, vendor):
        print("Statistics...")
        for SucStr in self.successStr:
            print(SucStr)
        if not len(self.Failed) == 0:
            print("Failed Downloads:")
            for strings in self.Failed:
                print(strings)
        else:
            print("Failed Downloads:None")
        print("\nTotal Time: "+str(self.timeDelta)+"min")
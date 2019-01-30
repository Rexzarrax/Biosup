import os
import time

class datastatistics:
    def __init__(self, vendor):
        self.timeEnd = 0
        self.timeDelta = 0
        self.Failed = []
        self.timeStart = time.time()
        self.successStr = []
        self.successCount = {}
        for ven2 in vendor:
            self.successCount[ven2] = 0
        print(self.successCount)

    def statistics(self, myData, vendor, ven, modelStr, success):
        cpathchq = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/BIOSHERE/"+vendor+"/"+str(modelStr)+".zip"
        if success or os.path.exists(cpathchq):
#            for model1 in myData.allVenArr[ven]:
            self.successCount[vendor] += 1
        else:
            self.Failed.append(modelStr)
    
    def printstat(self, vendor, myData):
        print("Statistics...")
        for ven2 in range(len(self.successCount)): 
            self.successStr.append(vendor[ven2]+": Successful Download's: "+str(self.successCount[vendor[ven2]])+"/"+str(len(myData.allVenArr[ven2])))
        self.timeEnd = time.time()
        self.timeDelta = int((self.timeEnd - self.timeStart)/60)
        for SucStr in self.successStr:
            print(SucStr)
        if not len(self.Failed) == 0:
            print("\nFailed Downloads:")
            for strings in self.Failed:
                print(strings)
        else:
            print("\nFailed Downloads: None")
        print("\nTotal Time: "+str(self.timeDelta)+"min")
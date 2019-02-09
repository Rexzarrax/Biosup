import os
import time

class datastatistics:
    def __init__(self, vendor):
        self.timeDelta = 0
        self.timeStart = time.time()

        self.failedModel = []
        self.successDownload = []
        self.alreadyDownload = []
        self.successCount = {}
        for ven2 in vendor:
            self.successCount[ven2] = 0
        print(self.successCount)

    def statistics(self, myData, vendor, ven, modelStr, status):
        cpathchq = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/BIOSHERE/"+vendor+"/"+str(modelStr)+".zip"
        if os.path.exists(cpathchq):
            self.successCount[vendor] += 1
        else:
            self.failedModel.append(modelStr)
    
    def printstat(self, vendor, myData):
        print("Statistics...")
        for ven2 in range(len(self.successCount)): 
            self.successDownload.append(vendor[ven2]+": Successful Download's: "+str(self.successCount[vendor[ven2]])+"/"+str(len(myData.allVenArr[ven2])))

        self.timeDelta = int((time.time() - self.timeStart)/60)

        for SucStr in self.successDownload:
            print(SucStr)

        if not len(self.failedModel) == 0:
            print("\nFailed Downloads:")
            for strings in self.failedModel:
                print(strings)
        else:
            print("\nFailed Downloads: None")
        print("\nTotal Time: "+str(self.timeDelta)+"min")
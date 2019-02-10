import os
import time

class datastatistics:
    def __init__(self, vendor):
        self.timeDelta = 0
        self.timeStart = time.time()

        self.failedDownloadList = []

        self.vendorCounts = {}
        for ven2 in vendor:
            self.vendorCounts[ven2] = {'successCount':0, 'failCount':0,'updateCount':0}
        #print(self.vendorCounts)
    
    def printstat(self, vendor, myData):
        print("Statistics...")
        for index,model in enumerate(myData.modelData):
            if myData.modelData[model]['status'] == 0:
                print('Nothing attempted on '+model)
                self.vendorCounts[myData.modelData[model]['vendor']]['failCount'] +=1
                self.failedDownloadList.append(model)
            elif myData.modelData[model]['status'] == 1:
                self.vendorCounts[myData.modelData[model]['vendor']]['successCount'] +=1
            elif myData.modelData[model]['status'] == 2:
                self.vendorCounts[myData.modelData[model]['vendor']]['failCount'] +=1
                self.failedDownloadList.append(model)
            elif myData.modelData[model]['status'] == 3:
                self.vendorCounts[myData.modelData[model]['vendor']]['updateCount'] +=1
            else:
                print('Corrupted status in '+myData.modelData[model])

        #print(str(self.vendorCounts))

        self.timeDelta = int((time.time() - self.timeStart)/60)

        for index,counter in enumerate(self.vendorCounts):
            print('=======%s======='% (counter))
            print('Successful downloads: %s' %(self.vendorCounts[counter]['successCount']))
            print('Already latest: %s' %(self.vendorCounts[counter]['updateCount']))
            print('Failed Downloads: %s' %(self.vendorCounts[counter]['failCount']))

        if not len(self.failedDownloadList) == 0:
            print("\nFailed Downloads:")
            for strings in self.failedDownloadList:
                print(strings)
        else:
            print("\nFailed Downloads: None")
        print("\nTotal Time: "+str(self.timeDelta)+"min")
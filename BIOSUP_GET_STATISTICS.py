import os
import time

class datastatistics:
    def __init__(self, vendor, dict_state_key):
        self.timeDelta = 0
        self.timeStart = time.time()
        self.dict_state_key = dict_state_key

        self.failedDownloadList = []

        self.vendorCounts = {}
        for ven2 in vendor:
            self.vendorCounts[ven2] = {'successCount':0, 'failCount':0,'updateCount':0}
        #print(self.vendorCounts)
    
    def printstat(self, vendor, myData):
        print("Statistics...")
        for index,model in enumerate(myData.dict_modelData):
            if myData.dict_modelData[model]['status'] == self.dict_state_key['no_action']:
                print('Nothing attempted on '+model)
                self.vendorCounts[myData.dict_modelData[model]['vendor']]['failCount'] +=1
                self.failedDownloadList.append(model)
            elif myData.dict_modelData[model]['status'] == self.dict_state_key['success_dl']:
                self.vendorCounts[myData.dict_modelData[model]['vendor']]['successCount'] +=1
            elif myData.dict_modelData[model]['status'] == self.dict_state_key['failed_dl']:
                self.vendorCounts[myData.dict_modelData[model]['vendor']]['failCount'] +=1
                self.failedDownloadList.append(model)
            elif myData.dict_modelData[model]['status'] == self.dict_state_key['up-to-date']:
                self.vendorCounts[myData.dict_modelData[model]['vendor']]['updateCount'] +=1
            elif myData.dict_modelData[model]['status'] == self.dict_state_key['ignore_bios']:
                pass
            elif myData.dict_modelData[model]['status'] == self.dict_state_key['update_bios']:
                pass
            else:
                print('Corrupted status in '+str(myData.dict_modelData[model]))

        #print(str(self.vendorCounts))

        self.timeDelta = int((time.time() - self.timeStart)/60)

        for int_index,str_counter in enumerate(self.vendorCounts):
            str_title = '{s:{c}^{n}}'.format(s=str_counter,n=20,c='=')
            print(str_title)
            print('Successful downloads: %s' %(self.vendorCounts[str_counter]['successCount']))
            print('Already latest: %s' %(self.vendorCounts[str_counter]['updateCount']))
            print('Failed Downloads: %s' %(self.vendorCounts[str_counter]['failCount']))

        if not len(self.failedDownloadList) == 0:
            print("\nFailed Downloads:")
            for strings in self.failedDownloadList:
                print(strings)
        else:
            print("\nFailed Downloads: None")
        print("\nTotal Time: "+str(self.timeDelta)+"min")
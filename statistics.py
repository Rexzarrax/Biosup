import os
import time

def statistics(myData, vendor, timeStart):
    print("Generating Statistics...")
    i = 0
    for ven3 in myData.allVenArr:
        modelCount = 0
        vendorstr = "----------"+vendor[i]
        print(vendorstr)
        for model1 in ven3:
            cpathchq = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/"+vendor[i]+"/"+str(model1).replace("/","-")+".zip"
            #print(cpathchq)
            if os.path.exists(cpathchq):
                modelCount += 1
            else:
                print("Failed to get: "+ model1)
        print("Successful DL's: "+str(modelCount)+"/"+str(len(ven3)))
        print(vendorstr+"\n")
        i+=1
            
    timeEnd = time.time()
    timeDelta = timeEnd - timeStart
    print("Total Time: "+str(int(timeDelta)/60)+"min")
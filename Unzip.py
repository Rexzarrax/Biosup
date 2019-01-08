import os
import zipfile


class unzip:
    def __init__(self):
        pass
    def deZip(self, file2unzip, folder2extract2):
        if os.path.exists(file2unzip):
            try:
                unzip = zipfile.ZipFile(file2unzip)
                unzip.extractall(folder2extract2)     
                unzip.close()
            except:
                print("Error in unziping...")
                print("Deleting culprit file ("+file2unzip+")...")
                os.remove(file2unzip)    
        else:
            print("File does not exist...")

import os
import zipfile


class unzip:
    def __init__(self):
        pass
    def deZip(self, file2unzip, folder2extract2):
        if os.path.exists(file2unzip):
            unzip = zipfile.ZipFile(file2unzip)
            unzip.extractall(folder2extract2)     
            unzip.close()
            #os.remove(file2unzip)
        else:
            print("File does not exist...")
import os
import zipfile


class unzip:
    def __init__(self):
        pass
    def deZip(self, file2unzip, folder2extract2):
        print("Attempting to unzip "+file2unzip+"...")
        if os.path.exists(file2unzip):
            with zipfile.ZipFile(file2unzip) as zip_file:
                try:
                    for member in zip_file.namelist():
                        if os.path.exists(folder2extract2 + r'/' + member) or os.path.isfile(folder2extract2 + r'/' + member):
                            print('File: ', member, ' already unzipped.')
                        else:
                            zip_file.extract(member, folder2extract2)
                except:
                    print("Error in unziping...")
                    print("Deleting culprit file ("+file2unzip+")...")
                    os.remove(file2unzip)    
        else:
            print("File does not exist...")

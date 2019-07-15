import os
import re
import requests
import urllib
from time import sleep
import html5lib
from selenium import webdriver
from time import sleep
try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 
from clint.textui import progress

#class holds methods for downloading the BIOS from a vendor
class biosDownload:
    def __Init__(self):
        pass
    def GenericUrlBuilder(self,dict_mymodel,uniqVendorData, str_cpath, driver, searchForLink):
        str_urlchq = uniqVendorData['vendorSort']
        URLaddON = uniqVendorData['vendorURLaddon']
        list_URLDLchq = uniqVendorData['vendorDownloadURLbase']
        bool_link_tester = True

        print("Finding "+dict_mymodel['name']+ " URL...")
        if not os.path.exists(str_cpath):
            #could add ability to use prod url is already in system but need to imp checking system
            while bool_link_tester:
                if dict_mymodel['productURL']=="":
                    print("Finding DL from URL: "+dict_mymodel['productURL'])
                    dict_mymodel['productURL'] = str(searchForLink.searchforlinkDDG(dict_mymodel['name'], str_urlchq))
                    dict_mymodel['productURL'] = re.sub(uniqVendorData['vendorSUBInput'],uniqVendorData['vendorSUBOutput'], dict_mymodel['productURL'], flags=re.IGNORECASE)
                    bool_link_tester = False
                else:
                    print("Using Prev found URL: "+dict_mymodel['productURL'])
                    bool_link_tester = True

                if not dict_mymodel['productURL'] == "None":
                    dict_mymodel['productURL'] += URLaddON
                    if self.getdlURL(driver, str_cpath, list_URLDLchq, dict_mymodel):
                        bool_link_tester = False
                else:
                    print("Error in getting Src URL")
                    bool_link_tester = False
        else:
            print("Zip file already downloaded...")

    #setup in future to try and use the url gathered from in dict_mymodel[productURL]
    #instead of using linksearching all the time
    def getdlURL(self, driver, str_cpath, list_urlChq, dict_mymodel):
        print("Motherboard URL: "+dict_mymodel['productURL'])
        print("Finding Download URL...")
        bool_gotLink = bool_refresh = False
        int_retries = 1
        while (bool_gotLink == False) and (int_retries < 5):
            soup_html = driver.getwebwithjs(dict_mymodel['productURL'], bool_refresh)
            for str_urlchq in list_urlChq:
                for link in soup_html.find_all('a', attrs={'href': re.compile(str_urlchq)}):
                    print("Found the URL:", link['href'])
                    str_download_Link = link['href']
                    if not link == "None":
                        bool_gotLink = True 
                        self.dlBIOS(str_download_Link,str_cpath, dict_mymodel)
                        break
                    break
            if not bool_gotLink:
                print("Missed URL, retrying, waiting "+str(int_retries-1)+"s...")
                sleep(int_retries)
                if int_retries >= 5:
                    bool_refresh = True 
                int_retries += 1
        if bool_gotLink:
            return True
        else:
            return False                                

    def dlBIOS(self,link,str_cpath, dict_mymodel):
        if not link == dict_mymodel['downloadURL']:
            try:             
                print("Download and Save to "+str_cpath)
                with open(str_cpath, 'wb') as file_zip:
                    req = requests.get(link, allow_redirects=True)
                    int_total_length = int(req.headers.get('content-length'))
                    for chunk in progress.bar(req.iter_content(chunk_size=1024), expected_size=(int_total_length/1024) + 1): 
                        if chunk:
                            file_zip.write(chunk)
                            file_zip.flush()
            except Exception as e:
                print("Error: "+str(e))
                    
            if os.path.exists(str_cpath):
                print("BIOS Successfully Downloaded...")
                dict_mymodel['downloadURL'] = link
                dict_mymodel['status'] = 4
            else:
                dict_mymodel['status'] = 3
        else:
            print("BIOS already up-to-date :)")
            dict_mymodel['status'] = 5
    


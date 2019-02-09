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
        self.status = {'DLSuccess':False,'DLUpdate':False}
    def GenericUrlBuilder(self,mymodel, urlchq, cpath, driver, dlURLchq, URLaddON, URLAlreadyGot, searchForLink):
        print("Finding "+mymodel+ " URL...")
        if not os.path.exists(cpath):
            prodURL = str(searchForLink.searchforlinkDDG(mymodel, urlchq))
            if not prodURL == "None":
                prodURL += URLaddON
                self.getdlURL(driver, prodURL, cpath, dlURLchq, mymodel, URLAlreadyGot)
            else:
                print("Error in getting Src URL")
        else:
            print("Zip file already downloaded...")
    #Download bios from Asus
    def urlBuilderAsus(self, mymodel, urlchq, cpath, driver,dlURLchq, URLAlreadyGot, searchForLink):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(searchForLink.searchforlinkDDG(mymodel, urlchq)).replace("/specifications","")
            prodURL = re.sub('_Download(.*)|_CPU(.*)|_QVL(.*)|_BIOS/','_BIOS', prodURL, flags=re.IGNORECASE)             
            if not prodURL == "None" :
                if not prodURL.endswith('_BIOS'):
                    print("Adding 'HelpDesk_BIOS/' to URL")
                    prodURL += '/HelpDesk_BIOS/'
                self.getdlURL(driver, prodURL, cpath, dlURLchq, mymodel, URLAlreadyGot)
            else:
                print("Error in getting Motherboard URL")      
        else:
             print("Zip file already downloaded...")


    def getdlURL(self, driver, prodURL, cpath, urlChq, mymodel, dlDict):
        print("Motherboard URL: "+prodURL)
        print("Finding Download URL...")
        gotLink = refresh = False
        retries = 1
        while (gotLink == False) and (retries < 5):
            soup_html = driver.getwebwithjs(prodURL, refresh)
            for link in soup_html.find_all('a', attrs={'href': re.compile(urlChq)}):
                print("Found the URL:", link['href'])
                if not link == "None":
                    gotLink = True 
                    self.dlBIOS(link, cpath, dlDict)
                    break
            if not gotLink:
                print("Missed URL, retrying, waiting "+str(retries-1)+"s...")
                sleep(retries)
                if retries >= 5:
                    refresh = True 
                retries += 1                                

    def dlBIOS(self, link, cpath, dlDict):
        self.status['DLSuccess'] = self.status['DLUpdate'] = False
        
        if not link['href'] in dlDict:
            try:             
                print("Download and Save to "+cpath)
                with open(cpath, 'wb') as f:
                    r = requests.get(link.get('href'), allow_redirects=True)
                    total_length = int(r.headers.get('content-length'))
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                        if chunk:
                            f.write(chunk)
                            f.flush()
            except Exception as e:
                print("Error: "+str(e))
                    
            if os.path.exists(cpath):
                print("BIOS Successfully Downloaded...")
                dlDict.append(link['href'])
                self.status['DLSuccess'] = True
        else:
            print("BIOS up-to-date :)")
            self.status['DLUpdate'] = True
    


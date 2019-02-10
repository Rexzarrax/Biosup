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
    def GenericUrlBuilder(self,mymodel, urlchq, cpath, driver, dlURLchq, URLaddON, searchForLink):
        print("Finding "+mymodel['name']+ " URL...")
        if not os.path.exists(cpath):
            mymodel['productURL'] = str(searchForLink.searchforlinkDDG(mymodel['name'], urlchq))
            if not mymodel['productURL'] == "None":
                mymodel['productURL'] += URLaddON
                self.getdlURL(driver, cpath, dlURLchq, mymodel)
            else:
                print("Error in getting Src URL")
        else:
            print("Zip file already downloaded...")
    #Download bios from Asus
    def urlBuilderAsus(self, mymodel, urlchq, cpath, driver,dlURLchq, searchForLink):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(searchForLink.searchforlinkDDG(mymodel['name'], urlchq)).replace("/specifications","")
            prodURL = re.sub('_Download(.*)|_CPU(.*)|_QVL(.*)|_BIOS/','_BIOS', prodURL, flags=re.IGNORECASE)             
            if not prodURL == "None" :
                if not prodURL.endswith('_BIOS'):
                    print("Adding 'HelpDesk_BIOS/' to URL")
                    prodURL += '/HelpDesk_BIOS/'
                mymodel['productURL'] = prodURL
                self.getdlURL(driver, cpath, dlURLchq, mymodel)
            else:
                print("Error in getting Motherboard URL")      
        else:
             print("Zip file already downloaded...")

    #setup in future to try and use the url gathered from in mymodel[productURL]
    #instead of using linksearching all the time
    def getdlURL(self, driver, cpath, urlChq, mymodel):
        print("Motherboard URL: "+mymodel['productURL'])
        print("Finding Download URL...")
        gotLink = refresh = False
        retries = 1
        while (gotLink == False) and (retries < 5):
            soup_html = driver.getwebwithjs(mymodel['productURL'], refresh)
            for link in soup_html.find_all('a', attrs={'href': re.compile(urlChq)}):
                print("Found the URL:", link['href'])
                downloadLink = link['href']
                if not link == "None":
                    gotLink = True 
                    self.dlBIOS(downloadLink,cpath, mymodel)
                    break
            if not gotLink:
                print("Missed URL, retrying, waiting "+str(retries-1)+"s...")
                sleep(retries)
                if retries >= 5:
                    refresh = True 
                retries += 1                                

    def dlBIOS(self,link ,cpath, mymodel):
        if not link == mymodel['downloadURL']:
            try:             
                print("Download and Save to "+cpath)
                with open(cpath, 'wb') as f:
                    r = requests.get(link, allow_redirects=True)
                    total_length = int(r.headers.get('content-length'))
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                        if chunk:
                            f.write(chunk)
                            f.flush()
            except Exception as e:
                print("Error: "+str(e))
                    
            if os.path.exists(cpath):
                print("BIOS Successfully Downloaded...")
                mymodel['downloadURL'] = link
                mymodel['status'] = 1
            else:
                mymodel['status'] = 2
        else:
            print("BIOS up-to-date :)")
            mymodel['status'] = 3
    


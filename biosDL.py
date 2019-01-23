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
    # def GenericUrlBuilder(self,vendor, mymodel, urlchq, cpath, driver, dlURLchq, URLaddON, linkSearching):
    #     print("Finding "+vendor+ " Motherboard product URL...")
    #     if not os.path.exists(cpath):
    #         prodURL = str(linkSearching.searchforlinkDDG(mymodel, urlchq))
    #         if not prodURL == "None":
    #             prodURL += URLaddON
    #             self.getdlURL(driver, prodURL, cpath, dlURLchq)
    #         else:
    #             print("Error in getting Src URL")
    #     else:
    #         print("Zip file already downloaded...")
    #Download bios from Asrock    
    def urlBuilderAsrock(self, mymodel, urlchq, cpath, driver, linkSearching):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(linkSearching.searchforlinkDDG(mymodel, urlchq))
            if not prodURL == "None":
                prodURL += "#BIOS"
                self.getdlURL(driver, prodURL, cpath, "^http://asrock.pc.cdn.bitgravity.com/BIOS/")
            else:
                print("Error in getting Src URL")
        else:
            print("ZipFile: "+cpath+" already downloaded.")
    
    #Download bios from Asus
    def urlBuilderAsus(self, mymodel, urlchq, cpath, driver, linkSearching):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(linkSearching.searchforlinkDDG(mymodel, urlchq)).replace("HelpDesk_Download/", "/HelpDesk_BIOS/").replace("/specifications","").replace("_CPU","_BIOS")              
            if not prodURL == "None" :
                if not prodURL.endswith('_BIOS/'):
                    print("Adding 'HelpDesk_BIOS/' to URL")
                    prodURL += '/HelpDesk_BIOS/'
                self.getdlURL(driver, prodURL, cpath, "^https://dlcdnets.asus.com/pub")
            else:
                print("Error in getting Motherboard URL")      
        else:
             print("Zip file already downloaded...")

    #Get link from Gigabyte
    def urlBuilderGigabyte(self, mymodel, urlchq, cpath, driver, linkSearching):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(linkSearching.searchforlinkDDG(mymodel, urlchq))
            #print(prodURL)
            if not str(prodURL) == "None":
                prodURL += "#support-dl-bios"
                self.getdlURL(driver, prodURL, cpath, "^http://download.gigabyte.asia/FileList/BIOS")                         
            else:
                prodURL = "Error in Search"


        else:
             print("Zip file already downloaded...")

    #get link from MSI
    def urlBuilderMSI(self, mymodel, urlchq, cpath, driver,linkSearching):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(linkSearching.searchforlinkDDG(mymodel, urlchq))
            if not str(prodURL) == "None":
                prodURL += "#down-bios"
                self.getdlURL(driver, prodURL, cpath, "^http://download.msi.com/bos")
            else:
                prodURL = "Error in Search"
        else:
             print("Zip file already downloaded...")

    def getdlURL(self, driver, prodURL, cpath, urlChq):
        print("Motherboard URL: "+prodURL)
        print("Finding Download URL...")
        gotLink = refresh = False
        retries = 1
        while (gotLink == False) and (retries < 11):
            soup_html = driver.getwebwithjs(prodURL, refresh)
            for link in soup_html.find_all('a', attrs={'href': re.compile(urlChq)}):
                print("Found the URL:", link['href'])
                if not link == "None":
                    gotLink = True 
                    self.dlBIOS(link, cpath)
                    break
            if not gotLink:
                print("Missed URL, retrying, waiting "+str(retries-1)+"s...")
                sleep(retries)
                if retries > 6:
                    refresh = True 
                retries += 1
                            

    def dlBIOS(self, link, cpath):
        try:             
            print("DL and Save to "+cpath)
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
            return True
  


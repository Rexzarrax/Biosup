import os
import re
import requests
from time import sleep
import html5lib
from selenium import webdriver

try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 
from clint.textui import progress

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 



#class holds methods for downloading the BIOS from a vendor
class bioufiDL:
    #Download bios from Asrock    
    def urlBuilderAsrock(self,myGetWeb, mymodel, urlchq, cpath, driver):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq))
            if not prodURL == "None":
                prodURL += "#BIOS"
                self.getdlURL(driver, prodURL, cpath, "^http://asrock.pc.cdn.bitgravity.com/BIOS/")
            else:
                print("Error in getting Src URL")
        else:
            print("already Downloaded Zip")
    
    #Download bios from Asus
    def urlBuilderAsus(self,myGetWeb, mymodel, urlchq, cpath, driver):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq))
            if not prodURL.endswith('HelpDesk_BIOS/'):        
                prodURL.replace('_Download/', '_BIOS/')
            if prodURL != "None" and not prodURL.endswith('_Download/') and not prodURL.endswith('_BIOS/'):
                prodURL += 'HelpDesk_BIOS/'
            elif prodURL == "None":
                print("Err in getting link...")
            if not prodURL == "None":
                self.getdlURL(driver, prodURL, cpath, "^https://dlcdnets.asus.com/pub")
            else:
                print("Error in getting Motherboard URL")      
        else:
            print("already Downloaded\n")

    #Get link from Gigabyte
    def urlBuilderGigabyte(self,myGetWeb, mymodel, urlchq, cpath, driver):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel+" bios", urlchq))
            print(prodURL)
            if not str(prodURL) == "None":
                prodURL += "#support-dl-bios"
                self.getdlURL(driver, prodURL, cpath, "^http://download.gigabyte.asia/FileList/BIOS")                         
            else:
                prodURL = "Error in Search"


        else:
            print("already Downloaded\n")

    #get link from MSI
    def urlBuilderMSI(self,myGetWeb, mymodel, urlchq, cpath, driver):
        print("Finding Motherboard URL...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq))
            if not str(prodURL) == "None":
                prodURL += "#down-bios"
                self.getdlURL(driver, prodURL, cpath, "^http://download.msi.com/bos")
            else:
                prodURL = "Error in Search"
        else:
            print("already Downloaded\n")

    def getdlURL(self, driver, prodURL, cpath, urlChq):
        print("Motherboard URL: "+prodURL)
        print("Finding Download URL...")
        gotLink = False
        retries = 0
        while (gotLink == False):
            print("No. Cycles: "+str(retries))
            soup_html = driver.getwebwithjs(prodURL)
            for link in soup_html.find_all('a', attrs={'href': re.compile(urlChq)}):
                print("Found the URL:", link['href'])
                if not link == "None":
                    gotLink = True 
                    self.dlBIOS(link, cpath)
                    break 
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
        else:
            print("Download Failed...\n")
            text_file = open("ErrUnzip.txt", "a")
            text_file.write("Error Link: %s\n" % link)
            return False   

    def searchforlink(self, mymodel, urlchq):
        print("Searching for "+mymodel+ " bios")

        for j in search(mymodel+" bios", tld="com", num=5, start=0, stop=5, pause=2): 
            print("Checking "+j)
            if re.search(urlchq, j, re.IGNORECASE):
                if not j == "None":
                    return j
                else:
                    print("Error in search")

    def __Init__(self):
        pass

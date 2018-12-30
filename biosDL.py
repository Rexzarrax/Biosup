import os
import re
import requests
import time
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
    #Framework for future code compression
    def UniUrlBuilder(self, myGetWeb, mymodel, urlchq, cpath, dlFilter, extraURL):
        print("Getting Src...")
        #get html page
        if not os.path.exists(cpath):
            #print(mymodel+" : "+ urlchq)
            prodURL = str(self.searchforlink(mymodel, urlchq))
            if not prodURL.endswith(extraURL) and prodURL != "None":
                prodURL += extraURL
            print("Src URL: "+prodURL)
            if not prodURL == "None":
                print("Getting URL...")
                soup_html = self.getwebwithjs(prodURL)
                #print(soup_html)
                for link in soup_html.find_all('a', attrs={'href': re.compile(dlFilter)}):
                    print("Found the URL:", link['href'])
                    if self.dlBIOS(link, cpath):
                        break  
                    else:
                        pass
            else:
                print("Error in getting Src URL")      
        else:
            print("already Downloaded\n")
    #Download bios from Asrock    
    def urlBuilderAsrock(self,myGetWeb, mymodel, urlchq, cpath, driver):
        print("Getting Src...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq)).replace("index.asp","")+"BIOS.html"
            print("Src URL: "+prodURL)
            print("Getting URL...")
            html_page = myGetWeb.simple_get(prodURL)
            #select only the url
            soup_html = BeautifulSoup(html_page, "html5lib")
            for link in soup_html.find_all('a', attrs={'href': re.compile("^http://asrock.pc.cdn.bitgravity.com/BIOS/")}):
                print("Found the URL:", link['href'])
                if self.dlBIOS(link, cpath):
                    break        
        else:
            print("already Downloaded")
    
    #Download bios from Asus
    def urlBuilderAsus(self,myGetWeb, mymodel, urlchq, cpath, driver):
        print("Getting Src...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel, urlchq))
            #print(prodURL)
            if not prodURL.endswith('HelpDesk_BIOS/'):        
                prodURL.replace('_Download/', '_BIOS/')
            if prodURL != "None" and not prodURL.endswith('_Download/') and not prodURL.endswith('_BIOS/'):
                prodURL += 'HelpDesk_BIOS/'
            elif prodURL == "None":
                print("Err in getting link...")
          
            print("Src URL: "+prodURL)
            if not prodURL == "None":
                print("Getting URL...")
                soup_html = driver.getwebwithjs(prodURL)
                for link in soup_html.find_all('a', attrs={'href': re.compile("^https://dlcdnets.asus.com/pub")}):
                    print("Found the URL:", link['href'])
                    if self.dlBIOS(link, cpath):
                        break  
                    else:
                        pass
            else:
                print("Error in getting Src URL")      
        else:
            print("already Downloaded\n")

    #Get link from Gigabyte
    def urlBuilderGigabyte(self,myGetWeb, mymodel, urlchq, cpath, driver):
        print("Getting Src...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel+" bios", urlchq))
            print(prodURL)
            if not str(prodURL) == "None":
                prodURL += "#support-dl-bios"
                soup_html = driver.getwebwithjs(prodURL)
                print("Src URL: "+prodURL)
                print("Getting URL...")
                #print(soup_html)
                for link in soup_html.find_all('a', attrs={'href': re.compile("^http://download.gigabyte.asia/FileList/BIOS")}):
                    print("Found the URL:", link['href'])
                    if self.dlBIOS(link, cpath):
                        break  
                    else:
                        pass                          
            else:
                prodURL = "Err in Search"


        else:
            print("already Downloaded\n")

    #get link from MSI
    def urlBuilderMSI(self,myGetWeb, mymodel, urlchq, cpath, driver):
        print("Getting Src...")
        if not os.path.exists(cpath):
            prodURL = str(self.searchforlink(mymodel.replace("Z390-I", "Z390I"), urlchq))
            if not str(prodURL) == "None":
                prodURL += "#down-bios"
                soup_html = driver.getwebwithjs(prodURL)
                print("Src URL: "+prodURL)
                print("Getting URL...")
                #select only the url  
                #print(soup_html)
                for link in soup_html.find_all('a', attrs={'href': re.compile("^http://download.msi.com/bos")}):
                    print("Found the URL:", link['href'])
                    if self.dlBIOS(link, cpath):
                        break  
                    else:
                        pass      
            else:
                prodURL = "Err in Search"
        else:
            print("already Downloaded\n")

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
        print("Searching for "+mymodel)
        for j in search(mymodel+" bios", tld="co.in", num=10, stop=1, pause=2): 
            if re.search(urlchq, j, re.IGNORECASE):
                return j

    def __Init__(self):
        pass

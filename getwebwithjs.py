import time
from selenium import webdriver
try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 
class webwithjs:
    def getwebwithjs(self, link, refresh):           
            if (not link == "None") and (not link == self.tempURL):
                print("First Load of "+link+"...")
                self.driver.get(link)
                self.tempURL = link

            if refresh:
                print("Running Refresh...")
                self.driver.get(link)
            elif not link == self.tempURL:
                print("Error in Web Driver, Link= "+link)
            else:
                print("Previous request still loading...")
            time.sleep(self.sleepTimer)
            temp = BeautifulSoup(self.driver.page_source, "html5lib") #page_source fetches page after rendering is complete
            return temp
            
    def __init__(self, openBrowser, sleepTimer):
        self.tempURL = ""
        self.sleepTimer = sleepTimer
        print("sleep timer: "+str(sleepTimer))
        try:
            #if FireFox:
                #FireFox headless
            options = webdriver.firefox.options.Options()
            if not openBrowser:
                options.add_argument('-headless')
            self.driver = webdriver.Firefox(options=options)
            #else:
            #   self.runChromeDriver(openBrowser)
        except:
            self.runChromeDriver(openBrowser)
    def runChromeDriver(self, openBrowser):
         #Chrome Headless
            options = webdriver.ChromeOptions()
            if not openBrowser:
                options.add_argument('headless')
            options.add_argument('--log-level=3')
            self.driver = webdriver.Chrome(chrome_options=options)

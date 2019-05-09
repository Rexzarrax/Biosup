import time
from selenium import webdriver
try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 
class webwithjs:
    def getwebwithjs(self, str_link, bool_refresh):           
            if (not str_link == "None") and (not str_link == self.str_tempURL):
                print("First Load of "+str_link+"...")
                self.driver.get(str_link)
                self.str_tempURL = str_link

            if bool_refresh:
                print("Running Refresh...")
                self.driver.get(str_link)
            elif not str_link == self.str_tempURL:
                print("Error in Web Driver, str_Link= "+str_link)
            else:
                print("Previous request still loading...")
            time.sleep(self.sleepTimer)
            soup_temp = BeautifulSoup(self.driver.page_source, "html5lib") #page_source fetches page after rendering is complete
            return soup_temp
            
    def __init__(self, openBrowser, sleepTimer):
        self.str_tempURL = ""
        self.sleepTimer = sleepTimer
        print("sleep timer: "+str(sleepTimer))
        try:
            options = webdriver.firefox.options.Options()
            if not openBrowser:
                options.add_argument('-headless')
            self.driver = webdriver.Firefox(options=options)
        except:
            self.runChromeDriver(openBrowser)
    def runChromeDriver(self, openBrowser):
         #Chrome Headless
            options = webdriver.ChromeOptions()
            if not openBrowser:
                options.add_argument('headless')
            options.add_argument('--log-level=3')
            self.driver = webdriver.Chrome(chrome_options=options)

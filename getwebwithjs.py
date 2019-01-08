import time
from selenium import webdriver
try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 
class webwithjs:
    def getwebwithjs(self, link):           
            if not link == "None" or not link == self.tempURL:
                self.driver.get(link)
                self.tempURL = link
            elif not link == self.tempURL:
                print("Error in Web Driver, Link= "+link)
            else:
                print("Previous request still loading...")
            temp = BeautifulSoup(self.driver.page_source, "html5lib") #page_source fetches page after rendering is complete
            return temp
    def __init__(self, FireFox, openBrowser):
        self.tempURL = ""
        if FireFox:
            #FireFox headless
            options = webdriver.firefox.options.Options()
            if not openBrowser:
                options.add_argument('-headless')
            self.driver = webdriver.Firefox(options=options)
        else:
            #Chrome Headless
            options = webdriver.ChromeOptions()
            if not openBrowser:
                options.add_argument('headless')
            options.add_argument('--log-level=3')
            self.driver = webdriver.Chrome(chrome_options=options)
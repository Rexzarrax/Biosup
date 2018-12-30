import time
from selenium import webdriver
try: 
    from bs4 import BeautifulSoup
except ImportError:  
    print("No module named 'BeautifulSoup' found") 
class webwithjs:
    def getwebwithjs(self, link):           
            if not link == "None":
                self.driver.get(link)
                time.sleep(3)
            else:
                print("Error in Web Driver, Link= "+link)
            temp = BeautifulSoup(self.driver.page_source, "html5lib") #page_source fetches page after rendering is complete
            #self.driver.quit()
            return temp
    def __init__(self, FireFox):
        if FireFox:
            #FireFox headless
            options = webdriver.firefox.options.Options()
            options.add_argument('-headless')
            self.driver = webdriver.Firefox(options=options)
        else:
            #Chrome Headless
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('--log-level=3')
            self.driver = webdriver.Chrome(chrome_options=options)
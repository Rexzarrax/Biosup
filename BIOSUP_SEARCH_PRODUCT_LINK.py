import re
import requests
import html5lib
import urllib.parse
from difflib import SequenceMatcher
try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'googlesearch' found") 
from bs4 import BeautifulSoup

class searchForLink:
    def __init__(self):
            pass
    #convert this to use browser instead of get requests
    #if searchforlinkDDG fails, uses google instead
    def searchforlinkDDG(self, str_mymodel, str_urlchq):
        print("Running DDG search...")
        list_search_extras = [""," uefi", " bios", " support"]
        int_search_threshold = 0.6
        for int_x in range(0,len(list_search_extras)):
            int_numURL = 0
            print("Query addon: "+list_search_extras[int_x])
            str_url = "https://duckduckgo.com/html/?q="+str_mymodel+list_search_extras[int_x]
            print("DDG Gen link: "+str_url)
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}    

            try:
                req = requests.get(str_url, headers = headers).text
                soup_html = BeautifulSoup(req, 'html5lib')
                #print(soup_html)
                #for str_chq_link in soup_html.find_all('a', attrs={'href': re.compile(str_urlchq, re.IGNORECASE)}):
                for str_chq_link in soup_html.find_all('a', attrs={'class': "result__url"}):
                    str_link_to_return = str_chq_link['href']
                    str_link_to_return = urllib.parse.unquote_plus(str_link_to_return)
                    str_link_to_return = str_link_to_return.replace("/l/?kh=-1&uddg=","")
                   
                    print("Found the URL:", str_link_to_return)
                    print(str_urlchq+str_mymodel+" vs. "+str_link_to_return)
                    
                    #will need to fix this up a bit to accuratly find the correct url
                    if re.findall(str_urlchq, str_link_to_return, re.IGNORECASE):
                        int_match = SequenceMatcher("",str_link_to_return,str_urlchq+str_mymodel).ratio()
                        print(str(int_match))
                        if int_match > int_search_threshold:
                            return str_link_to_return

                    elif not int_numURL > 20:
                        int_numURL += 1
                        print("Tried str_chq_link "+str(int_numURL)+":"+str(str_link_to_return+"\n"+str(str_urlchq)))
                    
                    else:
                        break
                #if str_link_to_return == "":
            except:
                print("Failed, Switching to Google...")
                googleAttempt = self.search_for_link_google(str_mymodel, str_urlchq)
                return googleAttempt
        print("Switching to Google...")
        googleAttempt = self.search_for_link_google(str_mymodel, str_urlchq)
        return googleAttempt
    def search_for_link_google(self, str_mymodel, str_urlchq):
        print("Google searching for "+str_mymodel+ " +support bios")
        try:
            for str_link in search(str_mymodel+" bios", tld="com", num=5, start=0, stop=5, pause=4): 
                print("Checking "+str_link)
                if re.search(str_urlchq, str_link, re.IGNORECASE):
                    if not str_link == "None":
                        return str_link
                    else:
                        print("Error in search")
        except:
            print("Major error in Search")
    



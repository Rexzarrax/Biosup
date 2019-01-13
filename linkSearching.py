import re
import requests
import html5lib
import urllib.parse
try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'googlesearch' found") 
from bs4 import BeautifulSoup

class searchForLink:
    def __init__(self):
            pass
    def searchforlinkDDG(self, mymodel, urlchq):
        print("Running DDG search...")
        numURL = 0
        url = "https://duckduckgo.com/html/?q="+mymodel+" +support"
        r = requests.get(url).text
        soup_html = BeautifulSoup(r, 'html5lib')
        #for link in soup_html.find_all('a', attrs={'href': re.compile(urlchq, re.IGNORECASE)}):
        for link in soup_html.find_all('a', attrs={'class': "result__url"}):
            unLinked = link['href']
            unLinked = urllib.parse.unquote_plus(unLinked)
            unLinked = unLinked.replace("/l/?kh=-1&uddg=","")
            print("Found the URL:", unLinked)
            if re.findall(urlchq, unLinked, re.IGNORECASE) :
                return unLinked #make sure contains model in url
            elif not numURL > 15:
                numURL += 1
                print("Tried link "+str(numURL)+":"+str(unLinked+"\n"+str(urlchq)))
            else:
                break
        print("Switching to Google...")
        googleAttempt = self.searchforlinkgoogle(mymodel, urlchq)
        return googleAttempt

    def searchforlinkgoogle(self, mymodel, urlchq):
        print("Google searching for "+mymodel+ " +support bios")
        try:
            for j in search(mymodel+" bios", tld="com", num=5, start=0, stop=5, pause=4): 
                print("Checking "+j)
                if re.search(urlchq, j, re.IGNORECASE):
                    if not j == "None":
                        return j
                    else:
                        print("Error in search")
        except:
            print("Major error in Search")
    



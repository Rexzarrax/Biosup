import requests



class web_scraper:
    def __init__(self, *args, **kwargs):
        #return super().__init__(*args, **kwargs)
        pass
    def get_page(str_url):

        obj_page = requests.get(str_url)
        if not obj_page.status_code == 200:
            print("Error, code: "+str(obj_page.status_code))
        else:
            return obj_page.text


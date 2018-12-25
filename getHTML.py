import contextlib
import requests

#Collects the skus of the various mobo
class gethtml:
    def __init__(self):
        pass

    def simple_get(self, url):
        try:
            with contextlib.closing(requests.get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return "Not Valid HTML"

        except requests.exceptions.RequestException as e:
            print("Err: "+str(url) + str(e))
            return None


    def is_good_response(self, resp):
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 
                and content_type is not None 
                and content_type.find('html') > -1)


    def log_error(e):
        print(e)
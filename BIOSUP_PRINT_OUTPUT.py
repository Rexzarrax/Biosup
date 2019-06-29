import time
import os



class printOutput():
    def __init__(self, *args, **kwargs):
        self.bool_log_to_file = True
        self.str_file_name = str(time.time()).replace(".","")+".log"
        self.str_log_file_name = os.path.join("log",self.str_file_name)
        self.list_str_10 = []
        try:
            os.mkdir("log")
        except:
            pass
        #return super().__init__(*args, **kwargs)
    
    def print_msg(self, str_msg):
        self.list_str_10.append(str_msg)
        if len(self.list_str_10) == 10:
            with open (self.str_log_file_name,"a") as outfile:
                outfile.write(self.list_str_10)
            self.list_str_10 = []
        
        


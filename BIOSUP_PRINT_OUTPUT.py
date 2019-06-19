import time
import os



class printOutput():
    def __init__(self, *args, **kwargs):
        self.bool_log_to_file = True
        self.str_file_name = str(time.time()).replace(".","")+".log"
        self.str_log_file_name = os.path.join("log",self.str_file_name)
        os.mkdir("log")
        #return super().__init__(*args, **kwargs)
    
    def print_msg(self, str_msg):
        print(str_msg)
        if self.bool_log_to_file == True:
            with open (self.str_log_file_name,"a") as outfile:
                outfile.write(str_msg)

        
        


from time import sleep

class chq_status:
    def __init__(self):
        pass
    def meth_Checker(Thr_Biosup_run, TEXT_CTRL_STATUS, parent_conn):
            try:
                while Thr_Biosup_run.is_alive: 
                #TEXT_CTRL_STATUS.AppendText("Running as of "+str(dt.strftime('%H:%M:%S'))+"\n")
                    TEXT_CTRL_STATUS.AppendText(parent_conn.recv()+"\n")
                    TEXT_CTRL_STATUS.AppendText("test"+"\n")
                    sleep(1)
                TEXT_CTRL_STATUS.AppendText("Biosup Exited...")
            except Exception as e:
                TEXT_CTRL_STATUS.AppendText("Unable to run CHECKER thread...\n Error: "+str(e)+"\n")   
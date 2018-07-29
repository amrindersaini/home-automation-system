import os 
from multiprocessing import Pool 

processes = {'servoController.py','camera.py', 'app.py'}

def run_process(process):
    os.system('python {}'.format(process))

try:
    pool = Pool(processes = 3)
    pool.map(run_process, processes)
except KeyboardInterrupt: 
    pool.close()
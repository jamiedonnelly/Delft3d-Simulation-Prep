import os 
from delftfuncs import * 
import sys

## CLI arguments
START = str(sys.argv[1]).replace('_',' ')
END = str(sys.argv[2]).replace('_',' ')
Dt = sys.argv[3]
WIND = sys.argv[4]

BASE_DIR = '...\\SimPrep\\Base'
TARGET_DIR = '...\\SimPrep\\Sim'

##

if __name__=="__main__":
        
    # clear directory 
    os.system(f'del /Q {TARGET_DIR}')
    for file in [os.path.join(BASE_DIR,i) for i in os.listdir(BASE_DIR)]:
        os.system(f'copy "{file}" "{TARGET_DIR}"')
    
    # Create boundary files
    os.system(f'python boundaries.py "{START}" "{END}"')
    # Create wind files 
    if WIND=='True':
        os.system(f'python wind_prep.py "{START}" "{END}"')
        os.system(f'python mdfiles.py "{START}" {WIND} {Dt}')
    else:
        os.system(f'python mdfiles.py "{START}" {WIND} {Dt}')
    
    
    
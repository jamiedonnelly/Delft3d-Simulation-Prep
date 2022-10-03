from lib2to3.pgen2.token import STAR
import mysql.connector 
import numpy as np 
from dateutil import parser 
from datetime import datetime 
import matplotlib.pyplot as plt 
import os
from decimal import Decimal
from delftfuncs import * 
import sys

# Functions 
def collect_data(cursor,table,value,start,end):
    CMD = "SELECT {value} FROM {table} WHERE (datetime BETWEEN {start} AND {END}"
    cursor.execute(CMD.format(value=value,table=table,start=start,end=end))
    data = [i[0] for i in cursor.fetchall()]
    return data

def boundary_time_prep(start_datetime,end_datetime,series):
    total_delta = end_datetime - start_datetime
    minutes = int(total_delta.total_seconds()/60)
    return np.array([int(i) for i in np.linspace(0,minutes,len(series))])

def water_level_bnd(cur,target_directory,fname,start_date,end_date):
    boundaries = [f'West{i}' for i in range(1,9)]
    """for i in range(1,32):
        boundaries.append(f'North{i}')"""
    CMD = "SELECT * FROM {table} WHERE (datetime BETWEEN '{start}' AND '{end}');"
    cur.execute(CMD.format(table='sea_surface_height',start=start_date,end=end_date))
    data = np.array([np.array(i) for i in cur.fetchall()])
    time = boundary_time_prep(START,END,data)
    for i in range(1,len(boundaries)+1):
        create_bct(os.path.join(target_directory,f'{boundaries[i-1]}.bct'),f'Boundary Section : {i}',boundaries[i-1],REFTIME,time,data[:,i])
    bcts = [os.path.join(target_directory,f'{i}.bct') for i in boundaries]
    combine_bct(os.path.join(target_directory,f'{fname}'),bcts)
    for i in bcts:
        os.system(f'del "{i}"')

def spacevar_bnd(START,END):
    n_boundaries = [f'North{i}' for i in range(1,5,1)]
    w_boundaries = [f'West{i}' for i in range(1,9,1)]
    
    ### West boundaries
    west_height = []
    cur.execute(CMD.format(table=WAVE_VARS[0],start=START,end=END))
    dt = np.array([np.array(i) for i in cur.fetchall()])
    for i in range(1,9,1):
        west_height.append(dt[:,i])

    west_period = []
    cur.execute(CMD.format(table=WAVE_VARS[1],start=START,end=END))
    dt = np.array([np.array(i) for i in cur.fetchall()])
    for i in range(1,9,1):
        west_period.append(dt[:,i])
        
    west_direction = []
    cur.execute(CMD.format(table=WAVE_VARS[2],start=START,end=END))
    dt = np.array([np.array(i) for i in cur.fetchall()])
    for i in range(1,9,1):
        west_direction.append(dt[:,i])
        
    time = [i*60 for i in range(len(dt))]
    for i in range(len(w_boundaries)):
        create_bcw(os.path.join(BOUNDARY_DIR,f'{w_boundaries[i]}.bcw'),w_boundaries[i-1],REFTIME,time,west_height[i],west_period[i],west_direction[i],10)
    bcws = [os.path.join(BOUNDARY_DIR,f'{i}.bcw') for i in w_boundaries]
    combine_bcw(os.path.join(BOUNDARY_DIR,'west.bcw'),bcws)
    for i in bcws:
        os.system(f'del "{i}"')

    ### North boundaries 
    north_height = []
    cur.execute(CMD.format(table=WAVE_VARS[0],start=START,end=END))
    dt = np.array([np.array(i) for i in cur.fetchall()])
    for i in range(40,dt.shape[1]):
        north_height.append(dt[:,i])

    north_period = []
    cur.execute(CMD.format(table=WAVE_VARS[1],start=START,end=END))
    dt = np.array([np.array(i) for i in cur.fetchall()])
    for i in range(40,dt.shape[1]):
        north_period.append(dt[:,i])
        
    north_direction = []
    cur.execute(CMD.format(table=WAVE_VARS[2],start=START,end=END))
    dt = np.array([np.array(i) for i in cur.fetchall()])
    for i in range(40,dt.shape[1]):
        north_direction.append(dt[:,i])
        
    time = [i*60 for i in range(len(dt))]
    for i in range(len(n_boundaries)):
        create_bcw(os.path.join(BOUNDARY_DIR,f'{n_boundaries[i]}.bcw'),n_boundaries[i-1],REFTIME,time,north_height[i],north_period[i],north_direction[i],10)
    bcws = [os.path.join(BOUNDARY_DIR,f'{i}.bcw') for i in n_boundaries]
    combine_bcw(os.path.join(BOUNDARY_DIR,'north.bcw'),bcws)
    for i in bcws:
        os.system(f'del "{i}"')
    
    ### Combine bcws
    bcws = [os.path.join(BOUNDARY_DIR,'west.bcw'),os.path.join(BOUNDARY_DIR,'north.bcw')]
    combine_bcw(os.path.join(BOUNDARY_DIR,'tst.bcw'),bcws)
    for i in bcws:
        os.system(f'del "{i}"')

# Constants 
BOUNDARIES = [f'West{i}' for i in range(1,9)]
for i in range(1,5):
    BOUNDARIES.append(f'North{i}')

BOUNDARY_DIR = "...\\SimPrep\\Sim"
WAVE_VARS = ['significant_wave_height','wave_period','wave_direction']

START = parser.parse(sys.argv[1])
END = parser.parse(sys.argv[2])

REFTIME = START.strftime('%Y%m%d')

CMD = "SELECT DISTINCT * FROM {table} WHERE (datetime BETWEEN '{start}' AND '{end}');"

if __name__=="__main__":

    # Load connection
    conn = mysql.connector.connect(host='',user='root',password='',database='boundaries')
    cur = conn.cursor()

    # Wave boundaries
    spacevar_bnd(START,END)

    ## Water level boundaries
    water_level_bnd(cur, BOUNDARY_DIR, 'tst.bct', START, END)
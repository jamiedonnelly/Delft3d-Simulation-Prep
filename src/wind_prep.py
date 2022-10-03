import os
from dateutil import parser
from datetime import datetime, tzinfo
from skimage.transform import resize 
import matplotlib.pyplot as plt 
import numpy as np 
import sys 
import boto3

# functions

# function transform data to full resolution

def findvals(data,index):
    neighbours=[]
    for i in range(index[0],-1,-1):
            if data[i,index[1]]!=-999:
                neighbours.append(data[i,index[1]])
                break
            else:
                pass
    for i in range(index[0],data.shape[0],1):
            if data[i,index[1]]!=-999:
                neighbours.append(data[i,index[1]])
                break
            else:
                pass
    for i in range(index[1],-1,-1):
        if data[index[0],i]!=-999:
            neighbours.append(data[index[0],i])
            break
        else:
            pass
    for i in range(index[1],data.shape[1],1):
        if data[index[0],i]!=-999:
            neighbours.append(data[index[0],i])
            break
        else:
            pass
    neighbours = np.array(neighbours)

    maxindex = 0
    for i in range(1,len(neighbours)):
        if abs(neighbours[i])>abs(neighbours[i-1]):
            maxindex = i
    return neighbours[maxindex]

def transform(data,shape=(25,25)):
    copy = np.ones_like(data)
    indexes = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i,j]==-999:
                indexes.append([i,j])
    for i,j in indexes:
        copy[i,j] = findvals(data,(i,j))
    for i,j in indexes:
        data[i,j] = copy[i,j]
    new = resize(data,shape)
    new[:,:2]=0
    new[:2,:]=0
    return new

def pressure_file(value,data,reftime,dt,directory):
    fname = 'tst.amp'
    with open(directory+fname,'w') as f:
        f.write("FileVersion = 1.03\n")
        f.write("filetype = meteo_on_equidistant_grid\n")
        f.write("NODATA_value = -999.0\n")
        f.write(f"n_cols = {data.shape[2]}\n")
        f.write(f"n_rows = {data.shape[1]}\n")
        f.write(f"grid_unit = degree\n")
        f.write("x_llcorner = -4.1643867356151\n")
        f.write("y_llcorner = 48.4895375177622\n")
        f.write(f"dx = 0.2640000000000004\n")        
        f.write(f"dy = 0.1147999999999999\n")     
        f.write("n_quantity = 1\n")
        f.write(f"quantity1 = air_pressure\n")
        f.write(f"unit1 = mbar\n")
        for i in range(data.shape[0]):
            f.write(f"TIME\t=\t{i*dt} minutes since {reftime.strftime('%Y-%m-%d %H:%M:%S')} +00:00\n")
            for k in range(data.shape[1]):
                f.write("\t".join([str(value) for i in range(data.shape[2])])+"\n")
        f.close()

def wind_file(data,reftime,dt,component,directory):
    assert data.ndim == 3
    if component=='u':
        fname='tst.amu'
        dir="x"
    elif component=='v':
        fname='tst.amv'
        dir="y"
    else:
        raise ValueError("Incorrect component argument.")
    with open(directory+fname,'w') as f:
        f.write("FileVersion = 1.03\n")
        f.write("filetype = meteo_on_equidistant_grid\n")
        f.write("NODATA_value = -999.0\n")
        f.write(f"n_cols = {data.shape[2]}\n")
        f.write(f"n_rows = {data.shape[1]}\n")
        f.write(f"grid_unit = degree\n")
        f.write("x_llcorner = -4.1643867356151\n")
        f.write("y_llcorner = 48.4895375177622\n")
        f.write(f"dx = 0.2640000000000004\n")        
        f.write(f"dy = 0.1147999999999999\n")        
        f.write("n_quantity = 1\n")
        f.write(f"quantity1 = {dir}_wind\n")
        f.write(f"unit1 = m s-1\n")
        for i in range(data.shape[0]):
            f.write(f"TIME\t=\t{i*dt} minutes since {reftime.strftime('%Y-%m-%d')} 00:00:00 +00:00\n")
            for k in range(data.shape[1]):
                f.write("\t".join([str(round(i,2)) for i in data[i,k,:]])+"\n")
        f.close()
        
## constants 

TARGET_DIR = '...\SimWind'

for file in os.listdir(TARGET_DIR):
    os.system(f'del "{os.path.join(TARGET_DIR,file)}"')

START = parser.parse(sys.argv[1].replace('_',' '),ignoretz=True) # start date 
END = parser.parse(sys.argv[2].replace('_',' '),ignoretz=True) # end date
    
###

if __name__=="__main__":
    
    session = boto3.Session( 
         aws_access_key_id='', 
         aws_secret_access_key='')
    s3 = session.resource('s3')
    bucket = s3.Bucket('windfiles')
    
    keys = []
    for object in bucket.objects.all():
        dt = parser.parse(object.key[:-4].replace('_',' '),ignoretz=True)
        if dt>=START:
            if dt<=END:
                keys.append(object.key)
            else:
                break
        else:
            pass
        
    for key in keys[::6]:
        bucket.download_file(key,os.path.join(TARGET_DIR,key))
    
    reftime = START
    files = [os.path.join(TARGET_DIR,i) for i in os.listdir(TARGET_DIR)]
        
    # transformed version 
    # replace dx,dy with 0.025 
    u_data = []
    v_data = []
    for i in files:
        with open(i,'rb') as f:
            dt = np.load(f)   
        u_data.append(transform(dt[0]))
        v_data.append(transform(dt[1]))

    u_data = np.array(u_data)
    v_data = np.array(v_data)

    wind_file(u_data,reftime,360,'u',"...\SimPrep\\Sim\\")
    wind_file(v_data,reftime,360,'v',"...\\SimPrep\\Sim\\")
    pressure_file(1000,u_data,reftime,360,"...\\SimPrep\\Sim\\")
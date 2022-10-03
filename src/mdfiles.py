import os
import sys 
from datetime import datetime
from dateutil import parser
from delftfuncs import scientific_notation

with open('Sim/tst.bct','r') as f:
    lines = f.readlines()
    MAX_T = lines[-1].split()[0]
    
with open('Sim/tst.bcw','r') as f:
    lines = f.readlines()
    for line in lines:
        if 'records-in-table' in line:
            NWAVES = int(line.split()[-1])
            
def insert_timepoint(lines,nwaves):
    for i in range(len(lines)):
        if '[Constants]' in lines[i]:
            break_index = break_index
    new_lines = lines[:break_index]
    for i in range(nwaves):
        new_lines.append('[TimePoint]')
        new_lines.append(" ".join(['  ','Time','\t',f'']))

START = parser.parse(str(sys.argv[1]).replace('_',' '))
MD_DATE = START.strftime('%Y-%m-%d')
VARYING = sys.argv[2] 
WIND = sys.argv[3]
Dt = sys.argv[-1]

# process mdw 
if WIND=='True': 
    with open('Base/var_mdw.txt','r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if 'ReferenceDate' in lines[i]:
                dt = lines[i].split()
                lines[i] = " ".join(['  ',dt[0],dt[1],f'{MD_DATE}','\n'])
    lines[8:8] = " ".join([' ',' MeteoFile','=','tst.amu','\n'])
    lines[8:8] = " ".join([' ',' MeteoFile','=','tst.amv','\n'])
    with open('Sim/tst.mdw','w') as f:
        for line in lines:
            f.write(line)
    f.close()
else:
    with open('Base/var_mdw.txt','r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if 'ReferenceDate' in lines[i]:
                dt = lines[i].split()
                lines[i] = " ".join(['  ',dt[0],dt[1],f'{MD_DATE}','\n'])
    with open('Sim/tst.mdw','w') as f:
        for line in lines:
            f.write(line)
    f.close()

    
# process mdf 
if WIND=="True":
    with open('Base/mdf.txt','r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if 'Itdate' in lines[i]:
                dt = lines[i].split()
                lines[i] = " ".join([dt[0],dt[1],f'#{MD_DATE}#','\n'])
            if 'Tstop' in lines[i]:
                dt = lines[i].split()
                lines[i] = " ".join([dt[0]+' ',dt[1],MAX_T,'\n'])
            if 'Dt' in lines[i]:
                dt = lines[i].split()
                lines[i] = " ".join([dt[0],'   ',dt[1],Dt,'\n'])
    lines[-2:-2] = " ".join(['Filwu','=','#tst.amu#','\n'])
    lines[-2:-2] = " ".join(['Filwv','=','#tst.amv#','\n'])
    lines[-2:-2] = " ".join(['Filwp','=','#tst.amp#','\n'])
    with open('Sim/tst.mdf','w') as f:
        for line in lines:
            f.write(line)
    f.close()
else:
    with open('Base/mdf.txt','r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if 'Itdate' in lines[i]:
                dt = lines[i].split()
                lines[i] = " ".join([dt[0],dt[1],f'#{MD_DATE}#'])
            if 'Tstop' in lines[i]:
                dt = lines[i].split()
                lines[i] = " ".join([dt[0]+' ',dt[1],MAX_T,'\n'])
            if 'Dt' in lines[i]:
                dt = lines[i].split()
                lines[i] = " ".join([dt[0],'   ',dt[1],Dt,'\n'])
    with open('Sim/tst.mdf','w') as f:
        for line in lines:
            f.write(line)
    f.close()
    


    
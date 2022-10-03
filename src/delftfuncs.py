from decimal import Decimal
import os 

## Convert values to scientific notation 

def scientific_notation(value):
    return "{:.7e}".format(Decimal(str(value)))

# Create space varying bcw file 

def spacevar_bcw(fname,boundary_name,nsplits,reftime,time,height,period,direction,dir_spreading):
    with open(fname,'w') as f:
        f.write(f"location\t\t'{boundary_name}'\n")
        f.write(f"time-function\t\t'non-equidistant'\n")
        f.write(f"reference-time\t\t{reftime}\n")
        f.write("time-unit\t\t'minutes'\n")
        f.write("interpolation\t\t'linear'\n")
        f.write("parameter\t\t'time'\t\tunit'[min]'\n")
        for i in range(nsplits):
            f.write("parameter\t\t'WaveHeight'\t\tunit'[m]'\n")
        for i in range(nsplits):
            f.write("parameter\t\t'Period'\t\tunit'[s]'\n")
        for i in range(nsplits):
            f.write("parameter\t\t'Direction'\t\tunit'[N^o]'\n")
        for i in range(nsplits):
            f.write("parameter\t\t'DirSpreading'\t\tunit'[-]'\n")
        for i in range(len(time)):
            entry = scientific_notation(time[i])+'\t'
            for j in range(nsplits):
                entry += scientific_notation(height[j][i]) + '\t'
            for j in range(nsplits):
                entry += scientific_notation(period[j][i]) + '\t'
            for j in range(nsplits):
                entry += scientific_notation(direction[j][i]) + '\t'  
            for j in range(nsplits):
                entry += scientific_notation(dir_spreading) + '\t' 
            entry += '\n'
            f.write(entry)
        return 

## Write .bcw file 

def create_bcw(fname,boundary_name,reftime,time,height,period,direction,dir_spreading):
    with open(fname,'w') as f:
        f.write(f"location\t\t'{boundary_name}'\n")
        f.write(f"time-function\t\t'non-equidistant'\n")
        f.write(f"reference-time\t\t{reftime}\n")
        f.write("time-unit\t\t'minutes'\n")
        f.write("interpolation\t\t'linear'\n")
        f.write("parameter\t\t'time'\t\tunit'[min]'\n")
        f.write("parameter\t\t'WaveHeight'\t\tunit'[m]'\n")
        f.write("parameter\t\t'Period'\t\tunit'[s]'\n")
        f.write("parameter\t\t'Direction'\t\tunit'[N^o]'\n")
        f.write("parameter\t\t'DirSpreading'\t\tunit'[-]'\n")
        f.write(f"records-in-table\t\t{len(time)}\n")
        for i in range(len(time)):
            entry = scientific_notation(time[i])+'\t'+scientific_notation(height[i]) \
                    +'\t'+scientific_notation(period[i])+'\t'+scientific_notation(direction[i]) \
                    +'\t'+scientific_notation(dir_spreading)+'\n'
            f.write(entry)
        return 

## Write .bct file

def create_bct(fname,table_name,boundary_name,ref_time,time,values):
    with open(fname,'w') as f:
        f.write(f"table-name\t\t'{table_name}'\n")
        f.write(f"contents\t\t\t'Uniform'\n")
        f.write(f"location\t\t\t'{boundary_name}'\n")
        f.write(f"time-function\t\t'non-equidistant'\n")
        f.write(f"reference-time\t\t{ref_time}\n")
        f.write("time-unit\t\t'minutes'\n")
        f.write("interpolation\t\t'linear'\n")
        f.write("parameter\t\t'time'\t\tunit'[min]'\n")
        f.write("parameter\t\t'water elevation (z) end A'\t\tunit'[min]'\n")
        f.write("parameter\t\t'water elevation (z) end B'\t\tunit'[min]'\n")
        f.write(f"records-in-table\t\t{len(time)}\n")
        for i in range(len(time)):
            entry = scientific_notation(time[i])+'\t'+scientific_notation(values[i])\
                    +'\t'+scientific_notation(values[i])+'\n'
            f.write(entry)
    return       

def combine_bct(fname,files: list):
    with open(fname,'w') as f:
        f.close()
    with open(fname,'a') as f:
        for file in files:
            with open(file,'r') as g:
                for line in g.readlines():
                    f.write(line)
                g.close()
        f.close()
    for i in files:
        os.system(f'del "{i}"')
    return 

def combine_bcw(fname,files: list):
    with open(fname,'w') as f:
        f.close()
    with open(fname,'a') as f:
        for file in files:
            with open(file,'r') as g:
                for line in g.readlines():
                    f.write(line)
                g.close()
    for i in files:
        os.system(f'del "{i}"')
        f.close()

## Write .wnd file

def create_wnd(fname,time,speed,direction):
    with open(fname,'w') as f:
        for i in range(len(time)):
            entry = scientific_notation(time[i])+'\t'+scientific_notation(speed[i])+'\t'\
                    +scientific_notation(direction[i])+'\n'
            f.write(entry)
    return







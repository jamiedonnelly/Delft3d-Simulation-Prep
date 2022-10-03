To use the functions in this folder to create a new folder just run create.py with the command line arguments. 
In total there are 6 CLI arguments 
1-Start date: written in format 'yyyy-mm-dd hh:mm:ss'
2-End date: written in format 'yyyy-mm-dd hh:mm:ss'
3-Time step (delta T): written as a number describing timestep in minutes
4-Varying boundaries (whether the wave boundaries should be uniform along the boundary or split into different sections: written as 'True' or 'False'
5-Wind: Whether to include wind and pressure in the simulation and the corresponding files written as 'True' or 'False'
6-Wind transform: Whether to transform the resolution of the wind files 'True' results in high-res wind and 'False' results in low-res wind

An example command would look like 

python ./create.py "'2005-01-01 00:00:00'" "'2005-02-01 00:00:00'" "5" "'True'" "'False'" "'False'"

For a simulation lasting from 2005/01/01 to 2005/02/01 with a 5 minute time step, spatially varying wave boundaries, no wind 
and no wind transformation. 


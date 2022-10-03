To use the functions in this folder to create a new folder just run create.py with the command line arguments. 
In total there are 4 CLI arguments 
1-Start date: written in format 'yyyy-mm-dd hh:mm:ss'
2-End date: written in format 'yyyy-mm-dd hh:mm:ss'
3-Time step (delta T): written as a number describing timestep in minutes
4-Wind: Whether to include wind and pressure in the simulation and the corresponding files written as True or False

An example command would look like 

python ./create.py '2005-01-01 00:00:00' '2005-02-01 00:00:00' 1 True

For a simulation lasting from 2005/01/01 to 2005/02/01 with a 1 minute time step and wind fields.

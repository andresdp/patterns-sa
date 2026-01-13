# Pipes and Filters

This folder contains models, scripts, data, and results of the [Pipes and Filters](https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters) design pattern.


## Print figures in the paper
Please, follow these steps to print the same figures presented in the paper for this design pattern:
1. Start a Jupyter notebook using <tt>jupyter notebook</tt>.
2. Open <tt>analysis.ipynb</tt>.
3. Execute all cells in that file.


## Reproduce results in the paper
To reproduce results presented in the paper, users can run new simulation. In this case, they should note that slightly different values may be observed due to the stochastic simulation. Please, follow these steps:
1. Run <tt>python3 runSim.py</tt> from the folder <tt>joint/</tt>.
2. Run <tt>python3 separated/runSim.py</tt> from the folder <tt>separated/</tt>.
3. Start a Jupyter notebook using <tt>jupyter notebook</tt> from the folder <tt>Pipes\_and\_Filters/</tt>.
4. Open <tt>analysis.ipynb</tt>.
5. Execute all cells in that file.


## Run provided models with different input parameters
Users can also tune input parameters of provided models to study different applications designed with the same patter.
Please, follow these steps to study your own applications with our model:
1. Open <tt>joint/runSim.py</tt>
2. Edit lines 55--70 with your input parameters (see the [Joint Parameter Table](#joint-parameter-table) for detailed explanation of available parameters) and save the file.
3. Open <tt>separated/runSim.py</tt>
4. Edit lines 55--72 with your input parameters (see the [Separated Parameter Table](#separated-parameter-table) for detailed explanation of available parameters) and save the file.
5. Run <tt>python3 runSim.py</tt> from the folder <tt>joint/</tt>.
6. Run <tt>python3 separated/runSim.py</tt> from the folder <tt>separated/</tt>.
7. Start a Jupyter notebook using <tt>jupyter notebook</tt> from the folder <tt>Pipes\_and\_Filters/</tt>.
8. Open <tt>analysis.ipynb</tt>.
9. Execute all cells in that file.

Note that all input parameters (except <tt>OUTFILE</tt>) are defined as lists to facilitate the execution of multiple simulation. If lists are not used, the tool will stop working. Use a list with *length = 1* to consider a single value for a parameter; otherwise, use a list with *length = N* to study your system with *N* different values for the considered parameter. 

The tool *combines* all provided input parameters and executes as many simulations as the total number of combinations of input parameters.


### Joint Parameter Table

| Parameter | Description |
| --- | --- |
| OUTFILE | Name of the file where simulation results will be stored |
| N\_TOT | Total number of requests in the system |
| N\_A | Number of type A requests in the system |
| Z\_A | Think time of type A requests |
| Z\_B | Think time of type B requests |
| C\_T1 | Number of CPUs allocated to task 1 |
| C\_T2 | Number of CPUs allocated to task 2 |
| C\_T3 | Number of CPUs allocated to task 3 |
| C\_T4 | Number of CPUs allocated to task 4 |
| S\_A\_T1 | Service time of type A requests at task 1 |
| S\_B\_T1 | Service time of type B requests at task 1 |
| S\_A\_T2 | Service time of type A requests at task 2 |
| S\_B\_T2 | Service time of type B requests at task 2 |
| S\_A\_T3 | Service time of type A requests at task 3 |
| S\_B\_T4 | Service time of type B requests at task 4 |


### Separated Parameter Table

| Parameter | Description |
| --- | --- |
| OUTFILE | Name of the file where simulation results will be stored |
| N\_TOT | Total number of requests in the system |
| N\_A | Number of type A requests in the system |
| Z\_A | Think time of type A requests |
| Z\_B | Think time of type B requests |
| C\_A\_T1 | Number of CPUs allocated to task 1 of type A requests |
| C\_A\_T2 | Number of CPUs allocated to task 2 of type A requests |
| C\_A\_T3 | Number of CPUs allocated to task 3 of type A requests |
| C\_B\_T1 | Number of CPUs allocated to task 1 of type B requests |
| C\_B\_T2 | Number of CPUs allocated to task 2 of type B requests |
| C\_B\_T4 | Number of CPUs allocated to task 4 of type B requests |
| S\_A\_T1 | Service time of type A requests at task 1 |
| S\_A\_T2 | Service time of type A requests at task 2 |
| S\_A\_T3 | Service time of type A requests at task 3 |
| S\_B\_T1 | Service time of type B requests at task 1 |
| S\_B\_T2 | Service time of type B requests at task 2 |
| S\_B\_T4 | Service time of type B requests at task 4 |

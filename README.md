# 6tisch-adaptive-mcs
An extended 6TiSCH simulator for adaptive MCS TSCH networks.

1) To let the simulator generate a topoogy based on experiment input parameters file:

        python runSim.py --genTopology=1 --json=input-example.json
    
2) To let the MILP solve a TSCH schedule for the given topology in ilp.json, in the ilp_schedule.json file, do:

        python adaptsch-arrival.py ilp.json ilp_schedule.json

3) To let the simulator run the TSCH experiment, using the MILP schedule allocations, for the given experiment file, do:

        python runSim.py --json=input-example.json --ilpfile=ilp.json --ilpschedule=ilp_schedule.json

The output of the simulation can be found in:
- bin/SimData/output_cpu0.dat
- bin/SimData/consumption.json
- bin/SimData/ilp_solution.json



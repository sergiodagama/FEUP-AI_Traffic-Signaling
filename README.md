
# FEUP Artificial Intelligence 1º pratical work

## Traffic Signaling Problem

### Group: 66_3A:
- Francisco Pires
- Pedro Nunes
- Sérgio da Gama

# Structure of the project:

We chose to develop our code in python as it is the most used language in AI aplications.
We have organized our project into 2 main subdirectories: src and docs.
Inside docs we have another three directories: city_plans and schedules.

On city_plans we store the files with data about the problem with the extension .txt as specified in the "Input Data Set" section on the project statement. When available, the files with extension .coords allow for the animation of the simulation on that city_plan.
On schedules we save the output state given by our algorithms,
when loaded  the user must ensure that the schedule is meant for the city_plan in use or else the program will terminate abruptly.

On the src directory we have the source files of our project and a subdirectory city_plan_generator containing a simple script for generating new maps with coordinates so that we could test our implementation with other maps other than the one on the project specification. This subproject generates new maps and puts them in its own city_plans subdirectory and if possible generates a .png of the map on the subdirectory city_plans_map.


# Execution

## Random Map Generator

Altough it 's not the objective of the project, if you wish to try the map generator to test the Traffic Signaling project set your working directory to src\city_plan_generator and run RandomMapGen.py.

    E.g. python3 RandomMapGen.py 10 10 10 100 1000 6 3 5 "example"
It takes the following parameters with default values:

- sim_time[=10] - total running time for simulation;
-  num_of_nodes[=10] - total number of nodes;
- num_of_cars[=10] - total number of cars;
- min_dist_sq[=100] - to ensure the nodes (intersections) are not too close together the program ensures that the square of the distance between any 2 nodes is more than this value;
 bonus[=1000] - the points given for every car that completely traverses its path;
 - max_street_cost[=6] - maximum cost to traverse a given street, that value while be a random integer between 1 and this value;
 - min_street_len[=3] - minimum lenght of the path given to any car;
 - max_street_len[=5] - maximum lenggth of the path given to any car;
 - file_name[=''] - name of the file to be created with this new city_plan, if no string is passed it will simply not save so if you want to keep the results you will have to pass every parameter, it will also not allow to save with the name of already existing files):

If you like the newly generated map you may copy the .txt and .coords files from src\city_plan_generator\city_plans to the docs\city_plans directory to be used in the main project.

## Traffic Signaling

To run our project simply run main.py with the working directory on the project root.
    
    E.g. python3 src\main.py

It will prompt the user to choose a predefined city_map or to introduce the name of the file within the docs\city_plans they wish to run.

The user can then choose to execute one of the 3 implemented algorithms and, if they wish, to save the resulting state to the docs\schedules directory or to run a previously saved traffic light schedule.
When running a simulation of saved schedule states, if the previously chosen city_plan has a corresponding .coords file the program will ask the user if he wants to watch the step by step animation of the simulation execution.
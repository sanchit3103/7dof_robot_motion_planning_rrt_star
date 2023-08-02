# Gaussian and Informed Sampling based RRT* Motion Planning on a 7DOF Robot

<p align="justify">
This project focuses on an improvement over traditional RRT* for motion planning of higher DOF manipulator robots with an aim to reduce the memory and time consumption as well as overcome the slow convergence rate of RRT*. Random sampling in traditional RRT* is replaced by a heuristic based Gaussian sampler. Resultant path is optimized using path smoothing techniques. A comparative study between traditional RRT*, Informed RRT* and Gaussian Sampling based RRT* is also carried out to assess the convergence and quality. The shortest paths found by each method are shown in the results below.
</p>

## Project Report
[Sanchit Gupta, Kishore Nukala, 'Gaussian and Informed Sampling based RRT* Motion Planning on a 7DOF Robot', ECE 276C, Course Project, UCSD](https://github.com/sanchit3103/7dof_robot_motion_planning_rrt_star/blob/main/Project%20Report.pdf)

## Project implementation in form of GIF file

<p align="justify">
The GIF below shows the implementation of traditional RRT* algorithm for motion planning of 7 DOF Panda robot. 
  
</p>

<p align="center">
  
  <img src = "https://github.com/sanchit3103/7dof_robot_motion_planning_rrt_star/assets/4907348/237b3508-0b6a-4de5-954d-cea882ba5072" height="400"/>

</p>

<p align="justify">
The GIF below shows the implementation of Informed RRT* algorithm for motion planning of 7 DOF Panda robot. 
  
</p>

<p align="center">
  
  <img src = "https://github.com/sanchit3103/7dof_robot_motion_planning_rrt_star/assets/4907348/8665ed5a-5311-4ae8-a180-6fe15c321a46" height="400"/>

</p>

## Details to run the code

* <b> project_code.ipynb: </b> Notebook which includes the setting up of environment, plotting of configuration space and implementation of traditional RRT*, informed RRT* and Gaussian Sampling based RRT* algorithms.
* <b> coppeliasim_env.py: </b> API to access CoppeliaSim environment.
* <b> run_env.py: </b> Implementation of policy on Panda robot in CoppeliaSim environment using the API.

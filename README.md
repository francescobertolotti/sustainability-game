# sustainability-game

This repository contains the code of the agent-based implementation of a sustaniability game. Specifically, the code divides into two parts:
1. a .ipynb notebook to run and visualize the experiment;
2. the .py files containing the model.

The .py files respectively contains:
* agent: the dynamics of each agent;
* global_vars: the collection of output and the computation of global variables (i.e., brown blocks);
* go: the scheduling of the simulation;
* MODEL: the combination of setup and go that makes run the model, and the experimental settings;
* parameters: the parameters employed in the simulation;
* setup: how the model is initialize at time 0.

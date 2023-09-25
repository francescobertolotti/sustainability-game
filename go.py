# import libraries
from global_vars import *
from agent import * 
import random
import numpy

def go(par, gv, al):

    

    # 1 - agent turn
    for ag in al.agents_list: 
        ag.update_dec_making(par, gv, al)
        ag.decision_resource(par, gv, al)
        ag.decision_attack(par, gv, al)

    

    # 2 - blocks computing
    gv.brown_computing(par, gv, al)


    # 3 - death of agents
    agent_death(par, gv, al)


    # N - compute globals
    gv.compute_globals(al, par)





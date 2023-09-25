# import libraries
from agent import * 
from global_vars import *

def setup(par, gv, al):


    #create agents
    for _ in range(par.n_players):
        new_agent = agent(par, _)
        al.agents_list.append(new_agent)
        al.original_list.append(new_agent)

    # create network
    create_networks(par, gv, al)
    #for a in al.agents_list: a.neighbors = [ag for ag in al.agents_list if ag != a]

    #adjust globals
    adjust_globals(par, gv, al)




        







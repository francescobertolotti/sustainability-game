# IMPLEMENTATO IN 4 - 1 - la rete quando muore un agente si "rimargina" e crea un nuovo link fra due che non sono collegati, se possibile. SI prende il nuovo vicino fra i vicini di qeullo morto
# 2 - nel processo decisionale, la scelta di fare rossi dipende anche dal numero di rossi degli avversari
# 3 - potrei dover implementare delle decisioni 7 e 8 in cui si dismettono i rossi e si trasformano in neri o verdi
# FATTO 4 - quando un agente muore, la sua rete di vicini è ereditata dall'agente che l'ha sconfitto per ultimo, e allo stesso modo gli agenti che lo avevano vicino sostituiscono come vicino quello che l'ha sconfitto (a meno che non ci sia già)

from parameters import *
from global_vars import *
from agent import * 
from setup import *
from go import *

import numpy as np
import random
import pandas as pd

class model():
    def __init__(self, my_seed):
        
        random.seed(my_seed)
        np.random.seed(seed=my_seed)

        self.al = agents_list()
        self.par = parameters()
        self.gv = glob_vars(self.par)

    def run(self, my_seed):
        
        random.seed(my_seed)
        np.random.seed(seed=my_seed)


        setup(self.par, self.gv, self.al)

        while(self.gv.end_flag):
            go(self.par, self.gv, self.al)


        return self.gv



class experiment():

    def __init__(self, n_sim):

        self.n_sim = n_sim
        self.mod = None

        self.dict_res = {
                         # inputs 
                         'seed': [],
                         'network_type': [],
                         'n_connections': [],
                         'n_players': [],
                         'init_brown': [], 
                         'length_forecast': [],
                         'length_memory': [],
                         'pref_ud_rate': [],

                         # outputs
                         'final_turn': [],
                         'n_players_final': [],
                         'blacks':[],
                         'greens':[],
                         'reds':[],
                         'browns':[],
                         'prop_blocks_surv': [],
                         'prop_attack_surv': [],
                         'rs_attack_surv': [],
                         'prop_blocks_death': [],
                         'prop_attack_death': [],
                         'rs_attack_death': []
                         }


    def generate_inputs(self,mod):
        
        mod.par.network_type = random.choice(['random_regular_graph','watts_strogatz_graph','barabasi_albert_graph'])
        mod.par.n_connections = 2 * np.random.randint(1,10)
        mod.par.n_players = np.random.randint(max(mod.par.n_connections + 1,10),200)
        mod.par.init_brown = np.random.randint(10000,100000)
        mod.par.length_forecast = np.random.randint(1,20)
        mod.par.length_memory = np.random.randint(2,20)
        mod.par.pref_ud_rate = np.random.random() * 0.2 

    def run_experiment(self):
        
        errors = 0
        for i in range(self.n_sim): 

            if i % 20 == 0 and i != 0: 
                print('sim ' + str(i) + ' of ' + str(self.n_sim), end = '\r')

            try:
                my_seed = random.randint(0,1000000)
                self.mod = model(my_seed)
                self.generate_inputs(self.mod)
                self.mod.run(my_seed)
                self.collect_results(my_seed)
            except:
                errors += 1
                print('error', end = '\r')
                continue

        self.dict_res = pd.DataFrame(self.dict_res)
        self.dict_res.to_csv('results_' + str(np.random.randint(0,99999999)) + '.csv', index = False)
        print("Simulation completed!!! There were " + str(errors) + " errors")

    def collect_results(self, my_seed):

        self.dict_res['seed'].append(my_seed)
        self.dict_res['network_type'].append(self.mod.par.network_type)
        self.dict_res['n_connections'].append(self.mod.par.n_connections)
        self.dict_res['n_players'].append(self.mod.par.n_players)
        self.dict_res['init_brown'].append(self.mod.par.init_brown)
        self.dict_res['length_forecast'].append(self.mod.par.length_forecast)
        self.dict_res['length_memory'].append(self.mod.par.length_memory)
        self.dict_res['pref_ud_rate'].append(self.mod.par.pref_ud_rate)

        self.dict_res['final_turn'].append(self.mod.gv.turn)
        self.dict_res['blacks'].append(self.mod.gv.ts_black[len(self.mod.gv.ts_black) - 1])
        self.dict_res['greens'].append(self.mod.gv.ts_green[len(self.mod.gv.ts_green) - 1])
        self.dict_res['reds'].append(self.mod.gv.ts_red[len(self.mod.gv.ts_red) - 1])
        self.dict_res['browns'].append(self.mod.gv.brown_ts[len(self.mod.gv.brown_ts) - 1])

        ag_survived = [ag for ag in self.mod.al.agents_list]
        ag_death = [ag for ag in self.mod.al.original_list if ag.survived == 0]
        
        self.dict_res['n_players_final'].append(len(ag_survived))
        self.dict_res['rs_attack_surv'].append(np.mean([ag.rs_attack for ag in ag_survived]))
        self.dict_res['rs_attack_death'].append(np.mean([ag.rs_attack for ag in ag_death]))
        
        new_prop_blocks_surv, new_prop_blocks_death,  = [],[]
        for _ in range(7):
            new_prop_blocks_surv.append(np.mean([ag.prop_blocks[_] for ag in ag_survived]))
            new_prop_blocks_death.append(np.mean([ag.prop_blocks[_] for ag in ag_death]))
        self.dict_res['prop_blocks_surv'].append(new_prop_blocks_surv)
        self.dict_res['prop_blocks_death'].append(new_prop_blocks_death)

        new_prop_attack_surv, new_prop_attack_death = [],[]
        for _ in range(3):
            new_prop_attack_surv.append(np.mean([ag.prop_attack[_] for ag in ag_survived]))
            new_prop_attack_death.append(np.mean([ag.prop_attack[_] for ag in ag_death]))
        self.dict_res['prop_attack_surv'].append(new_prop_attack_surv)
        self.dict_res['prop_attack_death'].append(new_prop_attack_death)

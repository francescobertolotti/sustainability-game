#import libraries
import numpy as np
import random
import networkx as nx

class agent:
    def __init__(self, par, who):
        self.who = who #number of the agent

        self.rs_resource = -1 + 2 * random.random() #level of brown on initial that scares it
        self.rs_attack = -1 + 2 * random.random() #shares of army on total that wants to have to defend
        #self.prop_blocks = [random.random() for i in range(7)] #propensions of the block productions
        #self.prop_attack = [random.random() for i in range(3)] #propensions of the block that other have that make them attackable
        self.prop_blocks = [min(max(np.random.normal(p[0],p[1]),0),1) for p in par.init_prop_blocks]
        self.prop_attack = [min(max(np.random.normal(p[0],p[1]),0),1) for p in par.init_prop_attack]
        self.black = par.init_black
        self.green = par.init_green
        self.red = par.init_red

        self.free_black = 0
        self.free_green = 0

        self.distroyed_black = 0
        self.distroyed_green = 0

        self.survived = 1
        self.winner = 0

        self.ts_black = [par.init_black]
        self.ts_green = [par.init_green]
        self.ts_red = [par.init_red]
        self.rs_resource_ts = [self.rs_resource]
        self.rs_attack_ts = [self.rs_attack]
        self.prop_blocks_ts = [self.prop_blocks]
        self.prop_attack_ts = [self.prop_attack]

        self.neighbors = []
        self.last_defeated_by = None

        # memory
        self.length_forecast = par.length_forecast
        self.length_memory = par.length_memory
        



        



    
    def decision_resource(self, par, gv, al):

        def implement_decision_resource(decision):
            
            tot_blocks = self.black + self.green + self.red

            if decision == 0: 
                self.free_black -= par.ip[0]
                if tot_blocks < par.max_blocks: self.black = self.black + 1
                
            if decision == 1: 
                self.free_green -= par.ip[1]
                self.black = self.black + 1
                self.green -= par.ip[1]

            if decision == 2: 
                self.free_black -= par.ip[2]
                self.green = self.green + 1
                self.black -= par.ip[2]

            if decision == 3: 
                self.free_green -= par.ip[3]
                if tot_blocks < par.max_blocks: self.green = self.green + 1

            if decision == 4: 
                self.free_green -= par.ip[4]
                if tot_blocks < par.max_blocks: self.red = self.red + 1

            if decision == 5: 
                self.free_black -= par.ip[3]
                if tot_blocks < par.max_blocks: self.red = self.red + 1

            if decision == 6: 
                self.free_green -= par.ip[6]
                gv.brown = min(gv.brown + 1, par.max_brown)



        #make the preferences according to the risk
        weigth_prop = [i for i in self.prop_blocks]
        for _ in range(len(weigth_prop)):
            if _ in [2,6,3]: weigth_prop[_] = weigth_prop[_] * ( 1 + min((gv.brown / par.init_brown),1) * self.rs_resource )
            if _ in [0,1,4,5]: weigth_prop[_] = weigth_prop[_] * ( 1 - min((gv.brown / par.init_brown),1) * self.rs_resource )
        weigth_prop = [min(max(wp,0),1) for wp in weigth_prop]
        #print(self.rs_resource, weigth_prop)
        
        #initialize the blocks still to be used
        self.free_black, self.free_green = self.black, self.green
        
        while self.free_black + self.free_green > 0:


            #revise the feasibility of the possible actions and change weigth_prop
            if par.ip[0] > self.free_black: weigth_prop[0] = 0
            if par.ip[1] > self.free_green: weigth_prop[1] = 0
            if par.ip[2] > self.free_black: weigth_prop[2] = 0
            if par.ip[3] > self.free_green: weigth_prop[3] = 0
            if par.ip[4] > self.free_green: weigth_prop[4] = 0
            if par.ip[5] > self.free_black: weigth_prop[5] = 0
            if par.ip[6] > self.free_green: weigth_prop[6] = 0
            #print(sum(weigth_prop))
            #if nothing feasible,leave the loop
            if sum(weigth_prop) == 0: 
                break

            #decide the action to do --> occhio che potrebbe dare errore
            #print(weigth_prop)
            decision = random.choices([0,1,2,3,4,5,6], weights = weigth_prop, k = 1)[0]
            #print("who: ", self.who, " dec: ", decision, " - fb: ", self.free_black, " - fg: ", self.free_green, " - b: ", self.black)
            implement_decision_resource(decision) 
            
            



            



        





    def decision_attack(self, par, gv, al):

        def implement_decision_attack(winner, loser):

            loser.last_defeated_by = winner

            winner.red -= decision.red
            loser.red = 0

            #take first black, than green
            temp_red = winner.red
            
            if temp_red <= loser.black:
                winner.black += temp_red
                loser.black -= temp_red
            else: 
                winner.black += loser.black 
                loser.black = 0
                temp_red -= loser.black 

                #then, if there are still reds that can conquest, take the green
                green_taken = min(loser.green, temp_red)
                winner.green += green_taken
                loser.green -= green_taken


        #decide if to attack
        mean_reds = np.mean([ag.red for ag in self.neighbors])
        #attack only if more than mean (normalized to talk with rs attack)
        if ( self.red - mean_reds ) / mean_reds > self.rs_attack: 
            
            other_players = [ag for ag in self.neighbors]
            #compute probability of attack a player with their blocks and my preferences
            prob_attack = [(ag.black * self.prop_attack[0] + ag.green * self.prop_attack[1] + ag.red * self.prop_attack[2]) for ag in other_players]
            #pick one
            if len(other_players) == 1:
                decision = other_players[0]
            else:
                if sum(prob_attack) == 0: prob_attack = [1 for _ in range(len(other_players))]
                decision = random.choices(other_players, weights = prob_attack, k = 1)[0]

            if self.red >= decision.red:
                implement_decision_attack(self, decision)
            else:
                implement_decision_attack(decision, self)
        
        


    def update_dec_making(self, par, gv, al):

        def update_ts_dec_making():
            #if brown_future / par.init_brown < rs_res_norm: print('out', self.who, self.prop_blocks)
            # at the end, update the time series for each agent of the preferences of the agents   
            self.rs_resource_ts.append(self.rs_resource)
            self.rs_attack_ts.append(self.rs_attack)
            #if brown_future / par.init_brown < rs_res_norm: print(gv.turn, self.who, self.prop_blocks_ts)
            self.prop_blocks_ts.append([self.prop_blocks[_] for _ in range(7)])
            #if brown_future / par.init_brown < rs_res_norm: print(gv.turn, self.who, self.prop_blocks_ts)
            self.prop_attack_ts.append(self.prop_attack)

        # update sustainability preferences
        if gv.turn <= self.length_memory: # do not update preferences if not enought time passed to take a decision
            update_ts_dec_making()
            return
        
        x = range(self.length_memory)
        y = gv.brown_ts[-self.length_memory:]
        par_line = np.polyfit(x,y,1)
        brown_future = (self.length_memory + self.length_forecast) * par_line[0] + par_line[1]

        rs_res_norm = self.rs_resource/ 2 + 0.5 # os it is between 0 and 1 and not -1 and 1
        if brown_future / par.init_brown < rs_res_norm:
            #print('in', self.who, self.prop_blocks)
            self.prop_blocks[0] *= 1 - par.pref_ud_rate
            self.prop_blocks[1] *= 1 - par.pref_ud_rate
            self.prop_blocks[2] = min(self.prop_blocks[2] + self.prop_blocks[2] * par.pref_ud_rate, 1)
            self.prop_blocks[3] = min(self.prop_blocks[3] + self.prop_blocks[3] * par.pref_ud_rate, 1)
            #self.prop_blocks[4] *= 1 - par.pref_ud_rate
            #self.prop_blocks[5] *= 1 - par.pref_ud_rate
            self.prop_blocks[6] = min(self.prop_blocks[6] + self.prop_blocks[6] * par.pref_ud_rate, 1)

            self.prop_attack[0] = min(self.prop_attack[0] + self.prop_attack[0] * par.pref_ud_rate, 1) # attack more the one with a lot of blacks
            self.prop_attack[1] *= 1 - par.pref_ud_rate # attack less the one with a lot of green
            self.prop_attack[2] = min(self.prop_attack[2] + self.prop_attack[2] * par.pref_ud_rate, 1) # attack less the one with a lot of reds

            #1 is the maximum values possible of risk aversion, the growth depends on how much is takes to reach that value
            self.rs_attack = self.rs_attack + (1 - self.rs_attack ) * par.pref_ud_rate 

            #print('out', self.who, self.prop_blocks)

        update_ts_dec_making()





def create_networks(par, gv, al):
    
    if par.network_type == 'random_regular_graph': G = nx.random_graphs.random_regular_graph(par.n_connections,len(al.original_list))
    if par.network_type == 'watts_strogatz_graph': G = nx.random_graphs.watts_strogatz_graph(len(al.original_list), par.n_connections, 0.1)
    if par.network_type == 'barabasi_albert_graph': G = nx.random_graphs.barabasi_albert_graph(len(al.original_list), par.n_connections)

    # assign neighbors to each agent
    for i, agent in enumerate(al.original_list):
        node_neighbors = list(G.neighbors(i))
        agent.neighbors = [al.original_list[node] for node in node_neighbors]



        
    




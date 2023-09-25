# import libraries

class parameters:
    def __init__(self):

        self.max_turn = 200
        self.n_players = 100

        #init parameters
        self.init_black = 2
        self.init_green = 0
        self.init_red = 0
        self.init_brown = 1000

        #init preferences
        self.init_prop_blocks = [[0.5,0.1],[0.5,0.1],[0.5,0.1],[0.5,0.1],[0.5,0.1],[0.5,0.1],[0.5,0.1]]
        self.init_prop_attack = [[0.5,0.1],[0.5,0.1],[0.5,0.1]]

        #network parameters
        self.network_type = 'random_regular_graph' #random_regular_graph, erdos_renyi_graph, cycle, scale-free, full_rary_tree
        self.n_connections = 5

        #investment parameters
        self.ip = [1,2,2,2,1,1,2]
        self.max_blocks = 500 
        self.max_brown = self.init_brown


        #brown consumption parameters
        self.brown_per_black = 1
        self.brown_per_red = 1

        #memory parameters
        self.pref_ud_rate = 0.05 # preference update rate
        self.length_forecast = 5
        self.length_memory = 5
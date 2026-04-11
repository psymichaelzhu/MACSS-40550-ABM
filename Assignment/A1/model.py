from mesa import Model
from mesa.space import SingleGrid
from agents import SchellingAgent
from mesa.datacollection import DataCollector
import numpy as np # [modification] 

class SchellingModel(Model):
    ## Define initiation, requiring all needed parameter inputs
    def __init__(self, growth_rate = 0.1, time_horizon = 3, width = 30, height = 30, density = 0.7, satisfaction_threshold = 0.5, group_one_share = 0.7, radius = 1, seed = None):
        ## Inherit seed trait from parent class and ensure seed is integer
        if seed is not None:
            seed = int(seed)
        super().__init__(rng=seed)
        ## Define parameter values for model instance
        self.growth_rate = growth_rate # [modification] growth rate of relationship happiness. For each dyad, happiness grows linearly with cumulative contact time. Growth rate is the slope.
        self.time_horizon = time_horizon # [modification] how much future steps to consider for happiness calculation. all agents have the same time horizon.
        self.width = width
        self.height = height
        self.density = density
        self.satisfaction_threshold = satisfaction_threshold # [modification] change the old name "desired_share_alike" to "satisfaction_threshold" to suit our new framing
        self.group_one_share = group_one_share
        self.radius = radius
        ## Create grid
        self.grid = SingleGrid(width, height, torus = True)
        ## Instantiate global happiness tracker
        self.happy = 0
        ## Place agents randomly around the grid, randomly assigning them to agent types.
        # [modification] @ line 39~48: introduce agent id, used to identify the agent in the contact matrix.
        ###################
        agent_id = 0 
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                if self.random.random() < self.group_one_share:
                    self.grid.place_agent(SchellingAgent(self, 1, agent_id), pos) 
                else:
                    self.grid.place_agent(SchellingAgent(self, 0, agent_id), pos)
                agent_id += 1
        ###################
        self.contact_matrix = np.zeros((len(self.agents), len(self.agents))) # [modification] contact matrix, used to store the contact history between agent dyads.
        ## Define data collector, to collect happy agents and share of agents currently happy
        self.datacollector = DataCollector(
            model_reporters = {
                "happy" : "happy",
                "share_happy" : lambda m : (m.happy / len(m.agents)) * 100
                if len(m.agents) > 0
                else 0, 
                # [modification] @ line 35~38: two measures
                ###################
                "average_contact_history" : lambda m : np.mean(m.contact_matrix[np.triu_indices_from(m.contact_matrix, k=1)]), # average contact history between all unique agent dyads (excluding diagonal)
                "average_segregation_score" : lambda m : np.mean([a.segregation_score for a in m.agents]), # average segregation score of all agents
                ###################
            }
        )
        ## Initialize datacollector
        self.datacollector.collect(self)

    ## Define a step: reset global happiness tracker, agents move in random order, collect data
    def step(self):
        self.happy = 0
        self.agents.shuffle_do("move")
        ## Run model until all agents are happy
        self.running = self.happy < len(self.agents)
        # [modification] @ line 65~78: update contact history matrix and define segregation scores
        ###################
        for agent in self.agents:
            # Update contact history matrix: how many steps two agents have been neighbors
            neighbors = agent.model.grid.get_neighbors(agent.pos, moore=True, radius=agent.model.radius, include_center=False)
            neighbor_ids = [n.id for n in neighbors]
            if neighbor_ids:
                agent.model.contact_matrix[agent.id, neighbor_ids] += 1
            # Define segregation score: proportion of neighbors of the same type; if no neighbors, score is 1
            if neighbors:   
                same_type_count = sum(1 for n in neighbors if n.type == agent.type)
                agent.segregation_score = same_type_count / len(neighbors)
            else:
                agent.segregation_score = 1
        ###################
        self.datacollector.collect(self)
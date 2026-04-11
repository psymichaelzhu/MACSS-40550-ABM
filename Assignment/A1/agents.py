from mesa import Agent

class SchellingAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, agent_type, agent_id):
        super().__init__(model)
        ## Set agent type
        self.type = agent_type
        self.id = agent_id # [modification] agent id, used to identify the agent in the contact matrix.
        self.segregation_score = 0 # [modification] segregation score, used to store the segregation score of the agent.
    ## Define basic decision rule
    def move(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore = True, radius = self.model.radius, include_center = False)
        # [modification] @ line 16~27: calculate expected satisfaction of this agent
        ###################
        # Assuming agents have perfect knowledge of growth rate (same as model parameter) and perfect memory of contact history.
        self.expected_satisfaction = 0 # here we use satisfaction instead of happiness to avoid confusion with the global happiness tracker.
        if len(neighbors) > 0:
            for neighbor in neighbors:
                base_satisfaction = 1 if neighbor.type == self.type else 0 # base satisfaction: 1 if the neighbor is of the same type, otherwise 0.
                contact_history = self.model.contact_matrix[self.id, neighbor.id] # contact history: the number of steps the agent has been neighbors with the neighbor (not including the current step).
                expected_contact_time = self.model.time_horizon + contact_history # expected contact time: the cumulative number of steps the agent will be neighbors with the neighbor until the end of the time horizon.
                expected_satisfaction = min(expected_contact_time * self.model.growth_rate + base_satisfaction, 1) # expected satisfaction at the end of the time horizon, a value between 0 and 1.
                self.expected_satisfaction += expected_satisfaction # update expected satisfaction of this agent
            self.expected_satisfaction /= len(neighbors) # average expected satisfaction of this agent
        ###################
        ## If not satisfied with neighbors, move to random empty slot. Otherwise add one to model count of happy agents.
        if self.expected_satisfaction < self.model.satisfaction_threshold: # [modification] naming convention consistency.
            self.model.grid.move_to_empty(self)
        else: 
            self.model.happy +=1


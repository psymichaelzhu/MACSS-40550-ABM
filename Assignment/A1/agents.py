from mesa import Agent

class SchellingAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, agent_type, agent_id):
        super().__init__(model)
        ## Set agent type
        self.type = agent_type
        self.id = agent_id # [modification] agent id, used to index the agent in the contact history matrix.
    ## Define basic decision rule
    def move(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore = True, radius = self.model.radius, include_center = False)
        # [modification] calculate expected satisfaction of this agent
        #<<<<<<<<<<<<<<<<<<<<<<<
        # Assuming agents have perfect knowledge of growth rate (same as environment parameter) and perfect memory of contact history.
        self.expected_satisfaction = 0
        if len(neighbors) > 0:
            for neighbor in neighbors:
                base_satisfaction = 1 if neighbor.type == self.type else 0 # satisfaction baseline according to the type matching: 1 if the neighbor is of the same type, otherwise 0.
                contact_history = self.model.contact_matrix[self.id, neighbor.id] # contact history: the number of steps this agent has been neighbors with that neighbor
                expected_contact_time = self.model.time_horizon + contact_history # expected contact time: the cumulative number of steps this agent will be neighbors with that neighbor, until the end of the time horizon.
                expected_satisfaction = min(expected_contact_time * self.model.growth_rate + base_satisfaction, 1) # expected satisfaction at the end of the time horizon, a value between 0 and 1.
                self.expected_satisfaction += expected_satisfaction # update expected satisfaction of this agent on this neighbor
            self.expected_satisfaction /= len(neighbors) # expected satisfaction of this agent, averaged over all neighbors.
        #>>>>>>>>>>>>>>>>>>>>>>>>>
        ## If not satisfied with neighbors, move to random empty slot. Otherwise add one to model count of happy agents.
        if self.expected_satisfaction < self.model.satisfaction_threshold: # [modification] naming
            self.model.grid.move_to_empty(self)
        else: 
            self.model.happy +=1


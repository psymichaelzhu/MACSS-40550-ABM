from mesa import Agent

class AudienceMember(Agent):
    def __init__(self, model, pos):
        super().__init__(model)
        # Set row and column according to the position
        # pos is (col, row) in Mesa's convention
        self.col = pos[0]
        self.row = pos[1]

        # Draw a private quality signal once at birth; never updated afterward.
        self.quality_signal = self.model.rng.random()

        # Phase-0 decision: stand immediately if quality meets the threshold
        self.standing = self.quality_signal >= self.model.threshold # since all agents share the same threshold, we consider it as a model-level parameter

    def social_update(self, snapshot = None):
        # Get SOP neighbors of the agent
        neighbors = self.model.get_SOP_neighbors(self.row, self.col) # It can be five- or cone-neighbor, depending on the model initialization

        # Count the total number of neighbors
        n_total = len(neighbors)

        # Count the number of standing neighbors, with the snapshot logic to handle the update order
        # if snapshot is provided, use the snapshot to count the number of standing neighbors
        # otherwise, use neighbors' current standing state (through the attribute `.standing`)
        if snapshot is None:
            n_standing = sum(1 for nb in neighbors if nb.standing)
        else:
            n_standing = sum(1 for nb in neighbors if snapshot[nb])
        
        # Phase-t>0 decision: apply majority rule heuristic
        # If a strict majority of visible neighbors are standing, the agent stands
        if n_standing > n_total / 2:
            self.standing = True
        # If a strict majority are seated, the agent sits
        elif n_standing < n_total / 2:
            self.standing = False
        # In the case of an exact tie, the agent chooses randomly
        else:
            self.standing = bool(self.model.rng.integers(0, 2))

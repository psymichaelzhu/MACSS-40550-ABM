from mesa import Model
from mesa.datacollection import DataCollector
from agents import AudienceMember
from mesa.space import SingleGrid


def _general_SOP_neighbors(row: int, col: int, n_rows: int, n_cols: int, k_limit: int | None = None) -> list[tuple[int, int]]:
    """
    helper function to get the SOP neighbors
    - if k_limit is None, considering all rows ahead, corresponds to the cone-neighborhood structure.
    - if k_limit=1, corresponds to the five-neighborhood structure.
    
    boundary truncation: seats that fall outside [0, n_rows) × [0, n_cols)
      are simply omitted — no wrap-around or padding is applied.
    """
    candidates = []

    # Same-row neighbours (left and right only)
    for dc in (-1, 1):
        c = col + dc
        candidates.append((row, c))

    # Forward rows: row-1, …, row-k_limit
    max_k = row if k_limit is None else min(k_limit, row) # if k_limit is None, considering all rows ahead
    for k in range(1, max_k + 1):         # k = how many rows ahead (≤ k_limit)
        target_row = row - k
        for dc in range(-k, k + 1):       # 2k+1 seats wide at k rows ahead
            c = col + dc
            candidates.append((target_row, c))

    # Only include valid coordinates (boundary truncation)
    coords = [(r, c) for r, c in candidates if 0 <= r < n_rows and 0 <= c < n_cols]
    return coords


class StandingOvationModel(Model):
    def __init__(self, n_rows=20, n_cols=20, threshold=0.5,
                 neighborhood="cone", update_order="async_incentive", seed=42):
        # set seed
        super().__init__(rng=seed)

        # auditorium dimensions
        self.n_rows = n_rows
        self.n_cols = n_cols
        # threshold for initial standing, shared by all agents
        self.threshold = threshold

        # neighborhood structure, can be 'five' or 'cone'
        self.neighborhood = neighborhood
        # updating order, can be 'synchronous', 'async_random', or 'async_incentive'
        self.update_order = update_order

        # whether the model has reached a steady state
        self.if_stable = False

        # build a 2-D seat grid, 0-based indexing
        self.grid = SingleGrid(n_cols, n_rows, torus=False) # note that in mesa grid, the order of dimensions is (cols, rows)
        # place agents on the grid
        for r in range(n_rows):
            for c in range(n_cols):
                agent = AudienceMember(self, (c, r))
                self.grid.place_agent(agent, (c, r))

        # record the initial majority direction (standing vs sitting)
        # for computation of informational efficiency
        init_standing = sum(1 for a in self.agents if a.standing) # initial number of standing agents
        self._initial_majority_standing = init_standing >= (n_rows * n_cols) / 2 # whether the initial majority is standing
        
        # private attribute `_prev_state_tuple` records the previous state to check if a steady state has been reached.
        # if the social-update phase produces no change at all, the model has reached a steady state.
        self._prev_state_tuple = tuple(a.standing for a in self.agents) # initialize as the initial state based on quality signal

        # data collector to collect the stand proportion and other metrics from the paper
        # here we don't use those metrics, but they can be used to reproduce the results in the paper.
        self.datacollector = DataCollector(
            model_reporters={
                "stand_proportion": lambda m: m._stand_proportion(),
                "final_NI":   lambda m: m.steps if m.if_stable else None,
                "final_SM":   lambda m: m._stick_in_muds() if m.if_stable else None,
                "final_IE":   lambda m: m._informational_efficiency() if m.if_stable else None,
            }
        )
        # Initialize data collector
        self.datacollector.collect(self)

    # use the general SOP neighbor helper function to get the neighbors
    def get_SOP_neighbors(self, row, col):
        if self.neighborhood == "five":
            coords = _general_SOP_neighbors(row, col, self.n_rows, self.n_cols, k_limit=1)
        elif self.neighborhood == "cone":
            coords = _general_SOP_neighbors(row, col, self.n_rows, self.n_cols, k_limit=None)
        else:
            raise ValueError(f"Invalid neighborhood structure: {self.neighborhood}")
        mesa_coords = [(c, r) for r, c in coords] # convert coordinates to mesa format (cols, rows)
        return self.grid.get_cell_list_contents(mesa_coords) # convert coordinates to agent objects via grid lookup

    def update_in_order(self):
        # async-incentive updating: agents surrounded by neighbors taking the opposite action are the first to update.
        if self.update_order == "async_incentive":
            order = list(self.agents)
            self.random.shuffle(order) # for tie-breaking
            # sort by incentive score from high to low
            order.sort(key=lambda agent: self._incentive_score(agent), reverse=True)
            # update the agents in this order
            for agent in order:
                agent.social_update()
        # async-random updating: agents update one at a time based on a random order
        elif self.update_order == "async_random":
            self.agents.shuffle_do("social_update")
        # synchronous updating: all agents update simultaneously
        elif self.update_order == "synchronous":
            # to achieve "real" synchronous updating, we store a snapshot of the current state
            # this avoids the later agents seeing the updated state of the earlier agents.
            snapshot = {a: a.standing for a in self.agents}
            # agents update based on the snapshot. 
            # specifically, they use the snapshot to count the number of standing neighbors
            for agent in self.agents:
                agent.social_update(snapshot)
        else:
            raise ValueError(f"Invalid update order: {self.update_order}")
            
    # compute the incentive score for an agent
    # incentive score: the proportion of neighbors that are not in the same standing state as the agent
    def _incentive_score(self, agent):
        nbs = self.get_SOP_neighbors(agent.row, agent.col)
        return sum(1 for nb in nbs if nb.standing != agent.standing) / len(nbs) if nbs else 0 # actually we don't need this fallback logic since the agent has at least one neighbor

    # compute the stand proportion
    def _stand_proportion(self):
        return sum(a.standing for a in self.agents) / (self.n_rows * self.n_cols)

    # compute the stick in muds proportion
    # stick in muds: the proportion of agents that are not in the majority direction
    def _stick_in_muds(self):
        standing_proportion = self._stand_proportion()
        if standing_proportion >= 0.5: # if the majority is standing, then return the sitting proportion
            return 1 - standing_proportion
        else: # if the majority is sitting, then return the standing proportion
            return standing_proportion

    # compute the informational efficiency
    # informational efficiency: whether the final majority is the same as the initial majority
    def _informational_efficiency(self):
        return (self._stand_proportion() >= 0.5) == self._initial_majority_standing

    def step(self):
        # update the agents in the specified order
        self.update_in_order()

        # check if the model has reached a steady state (every agent has the same standing state as the last step)
        current = tuple(a.standing for a in self.agents)
        if self._prev_state_tuple is not None and current == self._prev_state_tuple:
            self.if_stable = True
        # update the state tuple
        self._prev_state_tuple = current

        # collect data
        # the standing proportion is always collected
        # other metrics are collected only if the model has reached a steady state (otherwise None)
        self.datacollector.collect(self)

        # if the model has reached a steady state, stop running
        self.running = not self.if_stable
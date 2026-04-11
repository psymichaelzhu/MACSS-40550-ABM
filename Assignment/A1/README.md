1. contact record: a matrix (N_agent x N_agent), A_t[i,j] = cumulative number of steps those two agents have been neighbors at time t.
2. malleable relationship: happiness H(i,j) = min( (A_t[i,j]+T) * rate + base_happiness(i,j), 1) at the end of my time horizon, how much happiness I will get from this relationship.
3. T: time horizon, how much future steps to consider for happiness calculation.
3. base happiness: base_happiness(i,j) = 1 if color(i) == color(j), otherwise 0. If unlike, their initial interaction is likely to a negative experience, due to language barrier, cultural difference, etc.
4. individual happiness_t(i) = sum(H_t[i,k] for k in neighbors) / N_neighbors
5. happiness threshold: threshold = 0.5. If individual happiness_t(i) > threshold, the agent will stay in the location. Otherwise, the agent will relocate to a random place.



don't consider actual improvement, or updating of belief

one time step

static belief: growth or fixed

it will become better 
it won't change in the future





first class:


assuming perfect knowledge

line plot
    optimal



1. agent id
2. contact matrix
3. objective happiness function based on contact matrix: more contact, more happiness
4. subjective happiness function: assuming perfect knowledge; contact + time horizon
5. [same] threshold for happiness, move 





efficiency:
matrix
cache


realisitic: malleable relationship
however, it is still not enough to mitigate the segregation: converge, but still segregated

relational growth mindset is helpful:
converge without segregation

metric to quantify segregation
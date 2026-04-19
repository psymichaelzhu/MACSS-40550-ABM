# Relational Growth Mindset Mitigates Intergroup Segregation
## Introduction
Residential segregation based on social identity such as ethnicity remains a persistent feature of modern societies. A foundational explanation comes from Schelling's (1971) model, which shows that even mild in-group preference is sufficient to produce macro-level segregation. Yet the model assumes static relationship satisfaction, ignoring the fact that intergroup contact can improve attitudes over time.

The *contact hypothesis* (Allport, 1954) offers a corrective: sustained contact between members of different groups tends to reduce prejudice and increase mutual acceptance. In an agent-based framework, this suggests that satisfaction with a dissimilar neighbor should grow with the duration of co-residence — what we term the **contact model**.

The contact model, however, omits a psychological dimension: whether agents *believe* that cross-group relationships can improve through contact. Growth mindset theory (Dweck, 2006), originally proposed for intelligence, has been extended to interpersonal relationships as the *relationship growth mindset*: Agents who believe that relationship will improve over time may invest more in cross-group relationships, accelerating the process by which contact translates into acceptance.

We formalize and compare three agent-based models — the classic Schelling model, the contact model, and the growth mindset model — in terms of emergent intergroup segregation. 

Our central question is: **does believing that relationships can improve reduce segregation beyond what contact alone produces?** We hypothesize that the growth mindset will yield lower segregation than the other two conditions, suggesting that individual beliefs about relationship malleability — not just contact itself — may offer a lever for reducing segregation.

---

# Method

## Models

### Classic Schelling Model

**Setup.** Agents of two types are randomly placed on a grid. The satisfaction of a dyadic relationship is determined solely by type matching: same-type pairs have satisfaction 1, cross-type pairs have satisfaction 0.

**Decision rule** At each step, an agent computes its average satisfaction across all neighbor relationships. If this falls below a threshold, the agent relocates to a random empty cell.

**Termination condition** The model runs until all agents are satisfied with their neighbors.

**Core assumption** Relationship satisfaction is static and determined entirely by type similarity.

**Core parameters** 
- *Satisfaction threshold*: the minimum average satisfaction required for an agent to remain in place.


### Contact Model

**Setup** Same as the Schelling model, except that satisfaction in a dissimilar dyad grows linearly with the duration of co-residence rather than being fixed at 0.

**Decision rule** Same as the Schelling model.

**Termination condition** Same as the Schelling model.

**Core assumption** Intergroup contact reduces prejudice over time: satisfaction with a dissimilar neighbor increases when two agents have been co-residents.

**Core parameters**
- *Satisfaction threshold*: same as the Schelling model.
- *Growth rate*: the rate at which satisfaction of a dissimilar dyad increases per step of co-residence.


### Growth Mindset Model

**Setup** Same as the contact model.

**Decision rule** Agents are aware of the malleable nature of relationships. When computing satisfaction, each agent projects relationship satisfaction forward over a fixed time horizon and incorporates this expected future satisfaction into its current assessment.

**Termination condition** Same as the contact model.

**Core assumption** Following Dweck's (2006) growth mindset framework, agents who anticipate that relationships will improve are more willing to persist in cross-group co-residence, which in turn accelerates the transformation of contact into acceptance.

**Core parameters**
- *Satisfaction threshold*: same as the contact model.
- *Growth rate*: same as the contact model. We assume that agents have perfect knowledge of the growth process, therefore a single growth rate parameter applies to both the environment and the agents.
- *Time horizon*: the number of future steps agents consider when projecting relationship satisfaction.

[TODO]
> **Implementation note** Our implementation focuses on the growth mindset model, since it is the most general case, with growth rate and time horizon as parameters. The contact model is a special case with time horizon = 0, and the classic Schelling model is a special case with both growth rate = 0 and time horizon = 0. 

# Code Implementation
1. contact record: a matrix (N_agent x N_agent), A_t[i,j] = cumulative number of steps those two agents have been neighbors at time t.
2. malleable relationship: satisfaction H(i,j) = min( (A_t[i,j]+T) * rate + base_happiness(i,j), 1) at the end of my time horizon, how much happiness I will get from this relationship. T: time horizon, how much future steps to consider for satisfaction calculation.
2. base satisfaction: base_satisfaction(i,j) = 1 if color(i) == color(j), otherwise 0. If unlike, their initial interaction is likely to a negative experience, due to language barrier, cultural difference, etc.
3. individual satisfaction_t(i) = sum(H_t[i,k] for k in neighbors) / N_neighbors
4. satisfaction threshold. If individual satisfaction_t(i) > threshold, the agent will stay in the location. Otherwise, the agent will relocate to a random place.
[TODO] 写成pseudo code
---

# Results

[TODO]
When we consider a high satisfaction threshold (0.9),
1. In the *classic Schelling model* (growth rate = 0, time horizon = 0), the agents keep moving around the grid and never settle down.
2. In the *contact model* (growth rate = 0.4, time horizon = 10), the agents can settle down, but segregation emerges.
3. In the *growth mindset model* (growth rate = 0.4, time horizon = 10), the agents can settle down, without segregation. Actually, they are most likely to be satisfied with their initial neighbors.

As a summary, our simulation results found that the relational growth mindset ensures stable  without segregation. Instead, solely contact is not enough to reduce segregation.
We articulate this is because, in contact model, even contacts can improve relational satisfaction, but agents are myopic when making decisions. They only consider the current satisfaction, without considering the future satisfaction, which leaves contact no space to play a significant role in reducing segregation.
Our results suggest that, cultivating the belief that relationships can improve over time might be critical in reducing segregation, which provides a potential intervention for improving intergroup relations.

# References

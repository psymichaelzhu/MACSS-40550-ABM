# Relational Growth Mindset Mitigates Intergroup Segregation

## Introduction

Residential segregation based on social identity such as ethnicity remains a persistent feature of modern societies. A foundational explanation comes from Schelling's (1971) model, which shows that even mild in-group preference is sufficient to produce macro-level segregation. Yet the model assumes static relationship satisfaction, ignoring the fact that intergroup contact can improve attitudes over time.

The *contact hypothesis* (Allport, 1954) offers a corrective: sustained contact between members of different groups tends to reduce prejudice and increase mutual acceptance. In an agent-based framework, this suggests that satisfaction with a dissimilar neighbor should grow with the duration of co-residence — what we term the **contact model**.

The contact model, however, omits a psychological dimension: whether agents *believe* that cross-group relationships can improve through contact. Growth mindset theory (Dweck, 2006), originally proposed for intelligence, has been extended to interpersonal relationships as the *relationship growth mindset*: Agents who believe that relationships will improve over time may persist more in cross-group relationships, accelerating the process by which contact translates into acceptance.

We formalize and compare three agent-based models — the classic Schelling model, the contact model, and the growth mindset model — in terms of emergent intergroup segregation. 

Our central question is: **does believing that relationships can improve reduce segregation beyond what contact alone produces?** We hypothesize that the growth mindset will lead to faster stabilization and yield lower segregation than the other two conditions, suggesting that individual beliefs about relationship malleability — not just contact itself — may offer a lever for reducing segregation.

---

# Method

## Models

### Classic Schelling Model

**Setup.** Agents of two types are randomly placed on a grid. The satisfaction of a dyadic relationship is determined solely by type matching: same-type pairs have satisfaction 1, cross-type pairs have satisfaction 0.

> note: "satisfaction" refers to "happiness" in the original implementation

**Decision rule** At each step, an agent computes its average satisfaction across all neighbor relationships. If this falls below a threshold, the agent relocates to a random empty cell.

**Termination condition** The model runs until all agents are satisfied with their neighbors.

**Core assumption** Relationship satisfaction is static and determined entirely by type similarity.

**Core parameters** 

- *Satisfaction threshold*: the minimum average satisfaction required for an agent to remain in place.

### Contact Model

**Setup** Same as the Schelling model, except that satisfaction in a dissimilar dyad grows linearly with the duration of co-residence rather than being fixed at 0.

**Decision rule** Same as the Schelling model.

**Termination condition** Same as the Schelling model.

**Core assumption** Intergroup contact reduces prejudice over time: satisfaction increases when two dissimilar agents have been co-residents.

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



> **Implementation note** Our implementation focuses on the growth mindset model because it is the most general specification, with growth rate and time horizon as free parameters. The contact model is a special case in which time horizon = 0, meaning that agents account for past contact but do not project future improvement. The classic Schelling model is a further special case in which both growth rate = 0 and time horizon = 0, so satisfaction depends only on current neighbor composition.  
> To some extent, the traditional Schelling model considers only the present, the contact model incorporates memory of past interaction, and the growth mindset model additionally incorporates future-oriented evaluation.

---

# Results

To highlight the differences between the three models, we consider a high satisfaction threshold (0.9). This means that the agent is quite demanding in searching for a living environment.  
1.	In the classic Schelling model (growth rate = 0, time horizon = 0), agents keep moving around the grid and never settle down. The share of happy agents remains around 11%.  
2.	In the contact model (growth rate = 0.4, time horizon = 0), the share of happy agents gradually increases over time. After a relatively long period, the system eventually settles down, but the final pattern is still clearly segregated.  
3.	In the growth mindset model (growth rate = 0.4, time horizon = 10), agents are able to settle down without producing segregation. Most agents are already satisfied with their initial neighbors and therefore have little incentive to relocate.

Overall, our simulation results suggest that relational growth mindset can produce stability without segregation. Contact alone, by contrast, is not sufficient to substantially reduce segregation.  
We argue that this is because, in the contact model, contact does improve relationship satisfaction over time, but agents remain myopic in their decisions. If an agent has a certain number of dissimilar neighbors around, it tends to move away, so there is no chance to improve impression through contact, Therefore, the role of contact in preventing relationship segregation is limited.  
Our results therefore suggest that cultivating the belief that relationships can improve over time may be important for reducing segregation. This may offer a potential intervention perspective for improving intergroup relations.
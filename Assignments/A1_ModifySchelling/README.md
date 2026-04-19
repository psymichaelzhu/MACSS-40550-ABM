# Relational Growth Mindset: An Extension of the Schelling Model

**Abstract** This research extends the classic **Schelling Segregation Model** by introducing a **Relational Growth Mindset**. While the traditional model assumes agents make relocation decisions based on a static "snapshot" of their neighborhood, our framework incorporates an agent's belief that the quality of cross-group interactions can improve over time. By shifting from myopic evaluation to a forward-looking projection, we demonstrate how the belief in relational malleability can prevent "learning traps" and foster long-term social integration.

---

## 1. Research Question & Hypothesis

### 1.1 Research Question
In the classic Schelling model, preferences are fixed and immediate. In reality, social bonds are often forged through repeated contact. Does the belief that relationships can improve—independent of the actual rate of improvement—mitigate the emergence of macro-level segregation?

### 1.2 Hypothesis
A "Growth Mindset" will significantly reduce segregation levels. Specifically, a higher **improvement rate** ($r$) combined with a longer **planning horizon** ($H$) will allow agents to tolerate initial discomfort, eventually leading to more diverse, stable equilibrium states.

---

## 2. Introduction

### 2.1 The Problem of Myopia
In the original Schelling model, agents are effectively myopic. They evaluate their current surroundings, and if the proportion of "same-type" neighbors falls below a threshold, they move. This assumes that a neighborhood's quality is a fixed constant determined at $t=0$.

### 2.2 The Learning Trap
This static evaluation creates a **learning trap**: an agent who experiences a slightly uncomfortable cross-group interaction at the start will relocate immediately. By leaving, they forfeit the opportunity to learn that the relationship could have become positive over time. Segregation, therefore, arises not just from active prejudice, but from **premature withdrawal**.

### 2.3 Growth Mindset Integration
Our model introduces a forward-looking agent. Instead of asking "Am I happy now?", the agent asks, "Will I be happy here soon enough if I stay?"

---

## 3. Formal Framework

The decision logic is driven by two key parameters: the **improvement rate** ($r$) and the **time horizon** ($H$).

### 3.1 Relationship Utility
Let $u_{ij}(t)$ be the utility agent $i$ expects from neighbor $j$ after $t$ steps of interaction.
* **Same-type neighbors:** Utility is stable and high ($1$).
* **Unlike neighbors:** Utility starts at an initial value $u_0 < 1$ and grows linearly:

$$u_{ij}(t) = \min(u_0 + rt,\; 1)$$

### 3.2 Projected Neighborhood Happiness
Given a planning horizon $H$, the agent calculates the projected happiness of their current location rather than the current status:

$$\hat{h}_i(H) = \frac{1}{|N_i|} \sum_{j \in N_i} u_{ij}(H)$$

### 3.3 The Decision Rule
The relocation choice is determined by comparing this projection against the tolerance threshold $\tau$:

* **Stay:** If $\hat{h}_i(H) \geq \tau$
* **Move:** If $\hat{h}_i(H) < \tau$

> **Note:** The original Schelling model is recovered when $H=0$ or $r=0$.

---

## 4. Implementation & Computational Logic

### 4.1 Receding-Horizon Process
The model operates as a **receding-horizon process**. At each time step, agents project $H$ steps into the future based on the *current* neighborhood layout. Although neighbors might move in reality, the agent makes their current "stay vs. move" decision based on the assumption of local stability.

### 4.2 Algorithmic Optimization
To maintain computational tractability:
* **Localized Calculation:** Happiness is only re-calculated for an agent if they or one of their neighbors moved in the previous round.
* **Caching:** Stable neighborhoods use cached projection values, significantly speeding up large-scale simulations.

---

## 5. Expected Results

1.  **Lower Segregation Coefficients:** Systems with $r > 0$ and $H > 0$ reach equilibria with significantly higher diversity indices than the standard model.
2.  **The Horizon Effect:** Even small values of $r$ can prevent segregation if the time horizon $H$ is sufficiently long, allowing "temporary" discomfort to be out-weighed by "future" stability.
3.  **Threshold Sensitivity:** The growth mindset acts as a buffer, effectively lowering the functional tolerance threshold $\tau$ without changing the agent's core preference for similarity.

---

## 6. Limitations & Future Scope

While this model provides a more realistic psychological layer, it has constraints:
* **Exogenous Beliefs:** The mindset is currently a fixed parameter. In reality, a string of failed interactions might cause a "Growth" agent to revert to a "Fixed" mindset.
* **Lack of Generalization:** Interaction with one specific neighbor does not yet influence the agent's broad belief about the entire outgroup.
* **Temporal Discounting:** The model assumes future happiness at step $H$ is just as valuable as current happiness (no $1/e$ decay).

**Conclusion:** By shifting from static to forward-looking evaluation, we show that the "Learning Trap" is a primary driver of segregation. Encouraging a belief in the malleability of social bonds may be as effective as changing the bonds themselves.



# Research Question
Growth mindset, individual
Articulate on relationship
Schelling segregation, learning trap
actually change (contagent theory)
agent make decisions with those beliefs
Growth mindset faciliates integration?
Hypothesis

# Modification
## Conceptual
myopic estimation based on static snapshot
vs. 
malleable belief and projection (real)

## Math
one formula
multiple formula for belief increase integration


## Implement
Code change

## association
just a special case of horizon = 0 

# Implementation
## Efficiency consideration
local cache
add to current
actually will improve


# Result
visualization

## Discussion
### summary

### implication
time horizon --> longer time horizon (expected age ...)
mindset --> mobility

### Limitation
dynamic
generalization
temporal discounting

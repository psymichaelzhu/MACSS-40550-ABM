# Standing Ovation Model — Miller & Page (2004)

Mesa implementation of the Standing Ovation Problem.

> Miller, J. H., & Page, S. E. (2004). The standing ovation problem. *Complexity, 9*(5), 8–16. [https://doi.org/10.1002/cplx.20033](https://doi.org/10.1002/cplx.20033)

## File Overview


| File        | Description                                                                                                                       |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `agents.py` | `AudienceMember`: initial quality decision (t=0) and social majority-rule update (t>0)                                            |
| `model.py`  | `StandingOvationModel`: auditorium grid, neighborhood structure, update-order scheduler, convergence detection, metric collection |
| `app.py`    | Solara GUI: seat grid with stage, standing-proportion plot                                                                        |


## Reflection

### Implementation choices not fully specified in the paper

- **Boundary handling for neighborhoods.** The paper defines the five-neighbor and cone structures only for interior seats. For agents at the edge or in the front row, we apply simple truncation — seats outside the auditorium grid are omitted. 
- **Initial quality signal distribution.** The paper only states that `q_ij ∈ [0, 1]`, without specifying the sampling procedure. We draw each agent's signal independently from Uniform[0, 1].
- **Convergence criterion.** The paper reports "number of periods until a steady state is achieved" but does not define steady state precisely. We define it as two consecutive steps producing the identical agent-state vector (a tuple of all `standing` values). This is stricter than just checking the overall ratio, which might be the reason why we can't observe some situations (such as synchronous, cone) stablize as in the paper. `_prev_state_tuple` is initialized to the nonsocial decision state so convergence can be detected as early as step 1.
- **Operationalizing "incentive" in async-incentive updating.** The paper says agents "least like the people that surround them" move first, without giving a formula. We define incentive as the fraction of an agent's visible neighbours currently in the opposite state to her, and sort agents descending on that score. Ties are broken by a preliminary random shuffle.
- **Informational Efficiency as a run-level boolean.** The paper reports IE as a percentage across runs, but does not specify how it is computed within a single run. We define it as a boolean per run (whether final majority direction match initial majority direction).

### Implementation challenges

- **Coordinate system translation.** Mesa's `SingleGrid` uses `(col, row)` ordering, while our first implementation used `(row, col)`. Therefore, we need to translate the coordinates between the two systems.
- **Synchronous updating requires a full state snapshot.** True simultaneous updating means every agent must observe last step's world, not the partially-updated current state. This requires taking a dict snapshot of all agent states before any update occurs, then passing it into each agent's `social_update` call, rather than reading neighbours' `.standing` attributes directly.


## AI Usage Disclosure

Claude was used to assist with final code review (to detect potential bugs in scripts and inconsistencies in comments), language polish and structured formatting. 

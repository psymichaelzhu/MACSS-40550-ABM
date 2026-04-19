
# Main change statement
My main modification is to add "relational growth mindset", agents' belief about relationship malleability. Specifically, instead of assuming agents only make move decisions based on current state (match or mismatch), agents are now equiped with a belief of how much the interaction quality can improve across time. The remaining setup follows the original implementation.

# Comparison between two models

## Conceptual
In the basic setup of Schelling model, agents have a preference of the proportion of same-color neighbors. Agents are happy when there are sufficient proportion of same-color agents in their neighbors. If this preference is not satisfied, agents will move to a random place.

This basic setup assumes that agents are myopic, they only consider the initial match, while ignoring the malleable nature of relationship——maybe two people don't get along with each other at beginning because of their differences, but interaction might improve across constant contact over time. For example, two people might speak different languages, and conduct different cultural practices, which propose challenge at beginning of their interaction. But as time goes by, they can get to know each other better and then be able to coordinate in their interaction, which brings higher happiness.

## Implement
If an agent decide to move away, they lose the opportunity to interact with their (different-color) neighbors, and therefore won't be able to receive new feedback and update their impression. This phenomenon has been refered as learning trap effect, where agents cease updating once they've learned from the bad experience.

Zoom in to implementation details, in the original version, when make a move decision, agents' happiness sorely based on initial match or mismatch, which will influence their follow-up move decisions.
In a certain sense, agents are myopic, without considering the fact that interaction might be improved across more interactions.

$$sameness = sum(indicator same or not) (1)
happiness = sameness compared to threshold of sharelike (2)
move (3)$$

In contrast, in my modification, agents consider the potential improvement of relationship through 污染. 

(1)


one parameter will be time horizon
within 3 timesteps, can our relationship be improved?
after that improvement, can happiness exceed threshold?
If so, 保持现状(一个表达)


# Current model
## Parameter
- increase rate of happiness for unlike neighbors. After 1 round, my happiness with this neighbor will increase 0.01
- time horizon, how many steps to think forward. Consider 0 step--> classic version; consider more than 1 step --> growth

same to origin
- threshold (sharelike)
- ...


## Assumption:
when agent make this forward-thinking, planning
they assume neighbors don't move

since agents might actually relocate, which will violate the planning of last timepoint. So at each timepoint, agents will reconsider based on current layout

a math expression


# Efficiency consideration:
Each agents now involves heavier computation. But there are minor improvements we could make to allow the calculation to be more efficient.
If agents didn't move in the last round, we don't need to recalculate the happiness. Agent don't need to move. Which 
I add an additional conditional branch to each agent, tracking whether their neighbors have changed. If so, they stay the same place, and keep estimation the same; if changed, recalculate, through incremental.


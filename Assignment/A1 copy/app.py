import solara
from model import SchellingModel
from mesa.visualization import (  
    SolaraViz,
    make_space_component,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

## Define agent portrayal: color, shape, and size
def agent_portrayal(agent):
    return AgentPortrayalStyle(
        color = "blue" if agent.type == 1 else "red",
        marker= "s",
        size= 75,
    )

## Enumerate variable parameters in model: seed, grid dimensions, population density, agent preferences, vision, and relative size of groups.
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": {
        "type": "SliderInt",
        "value": 30,
        "label": "Width",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 30,
        "label": "Height",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "density": {
        "type": "SliderFloat",
        "value": 0.7,
        "label": "Population Density",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    # [modification] @ line 49~53: change name and default value
    #<<<<<<<<<<<<<<<<<<<<<<<
    "satisfaction_threshold": {
        "type": "SliderFloat",
        "value": 0.9, # we consider a high threshold
        "label": "Satisfaction Threshold",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    #>>>>>>>>>>>>>>>>>>>>>>>>>
    "group_one_share": {
        "type": "SliderFloat",
        "value": 0.7,
        "label": "Share Type 1 Agents",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "radius": {
        "type": "SliderInt",
        "value": 1,
        "label": "Vision Radius",
        "min": 1,
        "max": 5,
        "step": 1,
    },
    # [modification] @ line 73~78: new parameters
    #<<<<<<<<<<<<<<<<<<<<<<<
    "growth_rate": {
        "type": "SliderFloat",
        "value": 0.4,
        "label": "Growth Rate",
        "min": 0,
        "max": 1,
        "step": 0.05,
    },
    "time_horizon": {
        "type": "SliderInt",
        "value": 10,
        "label": "Time Horizon",
        "min": 0,
        "max": 10,
        "step": 1,
    },
    #>>>>>>>>>>>>>>>>>>>>>>>>>
}

## Instantiate model
schelling_model = SchellingModel()

## Define happiness over time plot
HappyPlot = make_plot_component({"share_happy": "tab:green"})

## Define space component
SpaceGraph = make_space_component(agent_portrayal, draw_grid=False)

# [modification] @ line 102~104: two additional plots
#<<<<<<<<<<<<<<<<<<<<<<<
ContactHistoryPlot = make_plot_component({"average_contact_history": "tab:blue"})
SegregationScorePlot = make_plot_component({"average_segregation_score": "tab:orange"})
BoundaryMixingPlot = make_plot_component({"boundary_mixing": "tab:purple"})
BoundarySegregationPlot = make_plot_component({"boundary_segregation": "tab:brown"})
#>>>>>>>>>>>>>>>>>>>>>>>>>


## Instantiate page inclusing all components
page = SolaraViz(
    schelling_model,
    components=[SpaceGraph, HappyPlot, ContactHistoryPlot, BoundarySegregationPlot], # [modification] new plots displayed
    model_params=model_params,
    name="Schelling Segregation Model",
)
## Return page
page
    
import solara
from model import StandingOvationModel
from mesa.visualization import (  
    SolaraViz,
    make_space_component,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

# Define agent portrayal: color, shape, and size
def agent_portrayal(agent):
    return AgentPortrayalStyle(
        color = "orange" if agent.standing else "blue",
        marker= "s",
        size= 100,
    )

# Modify the default grid visualization to show stage
# since in the standing ovation model, the location of stage is important.
def space_post_process(ax):
    # remove axis text / ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

    # add stage label on the row=0 side
    ax.text(
        0.5,
        -0.06,
        "▲ Stage ▲",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=11,
    )

# Enumerate variable parameters in model: seed, grid dimensions, threshold, neighborhood structure, and update mechanism.
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "n_rows": {
        "type": "SliderInt",
        "value": 20,
        "label": "Number of Rows",
        "min": 5,
        "max": 50,
        "step": 1,
    },
    "n_cols": {
        "type": "SliderInt",
        "value": 20,
        "label": "Number of Columns",
        "min": 5,
        "max": 50,
        "step": 1,
    },
    "threshold": {
        "type": "SliderFloat",
        "value": 0.5,
        "label": "Threshold of Quality Evaluation",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "neighborhood": {
        "type": "Select",
        "value": "cone",
        "label": "Neighborhood structure",
        "values": ["cone", "five"],
    },
    "update_order": {
        "type": "Select",
        "value": "async_incentive",
        "label": "Update mechanism",
        "values": ["async_incentive", "async_random", "synchronous"],
    }
}

# Instantiate model
standing_ovation_model = StandingOvationModel()

# Define standing proportion over time plot
StandingProportionPlot = make_plot_component({"stand_proportion": "tab:green"})

# Define audience grid component
SpaceGraph = make_space_component(agent_portrayal, draw_grid=False, post_process=space_post_process)

# Instantiate page including all components
page = SolaraViz(
    standing_ovation_model,
    components=[SpaceGraph, StandingProportionPlot],
    model_params=model_params,
    name="Standing Ovation Model",
)
# Return page
page
    
